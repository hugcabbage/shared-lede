#!/bin/sh

color_out() {
    if [ "$3" = "bold" ]; then
        printf "\e[1;$1m%s\e[0;0m\n" "$2"
    else
        printf "\e[0;$1m%s\e[0;0m\n" "$2"
    fi
}

red() {
    color_out 31 "$1" "$2"
}

green() {
    color_out 32 "$1" "$2"
}

yellow() {
    color_out 33 "$1" "$2"
}

blue() {
    color_out 34 "$1" "$2"
}

magenta() {
    color_out 35 "$1" "$2"
}

cyan() {
    color_out 36 "$1" "$2"
}

white() {
    color_out 37 "$1" "$2"
}
