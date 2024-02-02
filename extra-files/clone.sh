#!/usr/bin/env bash

get_value() {
    local key=$1
    local value

    value=$(yq -oy "$key" $file)
    if [ "$value" == "null" ]; then
        echo ""
    else
        echo "$value"
    fi
}

update_code() {
    local url=$1
    local path=$2
    local branch=$3
    local clone_flag=$4
    local switch_latest_tag=$5

    if [ -d "$path" ]; then
        cd $path
        echo "Local repository already exists, updating..."
        git pull
        cd - >/dev/null
    else
        echo "Local repository does not exist, cloning..."
        if [ -z "$branch" ]; then
            git clone $clone_flag $url $path
        else
            git clone $clone_flag -b $branch $url $path
        fi
    fi
    
    if [ "$switch_latest_tag" == "true" ]; then
        switch_to_latest_tag "$path"
    fi
}

update_base() {
    local base=$1
    local path=$2
    local url
    local branch
    local switch_latest_tag
    local single_branch
    local clone_flag

    url=$(get_value ".base.$base.url")
    branch=$(get_value ".base.$base.branch")
    switch_latest_tag=$(get_value ".base.$base.switch_latest_tag")
    clone_flag=$(get_value ".base.$base.clone_flag")

    if [ "$clone_flag" == "none" ]; then
        clone_flag=""
    else
        clone_flag="--single-branch"
    fi

    update_code "$url" "$path" "$branch" "$clone_flag" "$switch_latest_tag"
}

update_apps() {
    local base=$1
    local supply_dir=$2
    local b_dir=$3
    local url
    local branch
    local path
    local rsync
    local switch_for_lede
    local clone_flag
    local set_flag=false

    if [ "$base" == "lede" ]; then
        gvarg='.application.set'
        yqexpr=('.application.set | keys | join("\n")')
        set_flag=true
    else
        gvarg='.application'
        yqexpr=('.application | keys | map(select(. != "set")) | join("\n")')
    fi

    if [ "$set_flag" == true ]; then
        while IFS= read -r sapp; do
            echo "Cloning $sapp..."
            sexpr=$(get_value ".application.set-supply.$sapp")
            url=$(get_value "$sexpr.url")
            path=$supply_dir/$sapp

            update_code "$url" "$path" "" "$clone_flag" ""
        done < <(yq -oy '.application.set-supply | keys | join("\n")' $file)
    fi

    while IFS= read -r app; do
        echo "Cloning $app..."
        url=$(get_value "$gvarg.$app.url")
        branch=$(get_value "$gvarg.$app.branch")
        eval path=$(get_value "$gvarg.$app.path")
        rsync=$(get_value "$gvarg.$app.rsync")
        branch_for_lede=$(get_value "$gvarg.$app.branch_for_lede")
        clone_flag=$(get_value "$gvarg.$app.clone_flag")

        if [ -n "$branch_for_lede" -a "$base" == "lede" ]; then
            branch=$branch_for_lede
        fi

        if [ -z "$path" ]; then
            path=$supply_dir/$app
        fi

        if [ "$clone_flag" == "none" ]; then
            clone_flag=""
        else
            clone_flag="--depth 1"
        fi

        update_code "$url" "$path" "$branch" "$clone_flag" ""
        rsync_code "$rsync" "$path" "$supply_dir"
    done < <(yq -oy "${yqexpr[@]}" $file)
}

rsync_code() {
    local command=$1
    local path=$2
    local supply_dir=$3

    kind=$(yq '. | kind' <<<"$command")
    if [ "$kind" == "seq" ]; then
        while IFS= read -r item; do
            eval "$item"
        done < <(yq '. | join("\n")' <<<"$command")
    else
        eval "$command"
    fi
}

validate_base() {
    local base=$1

    if $(yq ".base | has(\"$base\")" $file); then
        return 0
    else
        return 1
    fi
}

switch_to_latest_tag() {
    local path=$1
    local latest_tag_hash
    local latest_tag

    cd $path
    latest_tag_hash=$(git rev-list --tags --max-count=1)
    if [ -z "$latest_tag_hash" ]; then
        echo "No tag to switch, keep the latest commit."
    else
        git checkout $latest_tag_hash
        latest_tag=$(git describe --tags $latest_tag_hash)
        echo "The code has been switched to the latest version $latest_tag."
    fi
    cd - >/dev/null
}

# ---mian---

select_flag=false

file=$1
if [ -z "$file" ]; then
    echo "Please enter toml file path:"
    read file
fi

base=$2
mapfile -t bases < <(yq -oy '.base | keys | join("\n")' $file)
if [ -z "$base" ]; then
    echo "To select a base code:"
    select base in "${bases[@]}"; do
        validate_base "$base" && break || echo "Please re-select."
    done
    select_flag=true
else
    validate_base "$base" || exit 1
fi

code_dir_new=$3
if [ -z "$code_dir_new" -a "$select_flag" == true ]; then
     echo "Please enter a base dir(can be blank):"
     read code_dir_new
fi

if [ -n "$code_dir_new" ]; then
    if [[ "$code_dir_new" != _test* ]]; then
        echo "base dir must be startwith '_test'!"
        exit 1
    else
        code_dir=$code_dir_new
    fi
else
    code_dir=$(get_value '.common.code_dir')
fi

eval supply_dir=$(get_value '.common.supply_dir')
eval b_dir=$(get_value '.common.b_dir')

update_base "$base" "$code_dir"
update_apps "$base" "$supply_dir" "$b_dir"

stdir=$(dirname $(realpath $0))
supply_path=$(realpath $supply_dir)
cd $code_dir

if ! grep -q "src-link supply $supply_path" feeds.conf.default; then
    echo "src-link supply $supply_path" >> feeds.conf.default
fi

./scripts/feeds update -a
./scripts/feeds install -a
$stdir/../preset-$base/1.modify.sh

cd - >/dev/null
