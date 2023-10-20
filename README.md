# 使用 GitHub Actions 快速定制编译 OpenWrt 固件

流程文档参考[KFERMercer/OpenWrt-CI](https://github.com/KFERMercer/OpenWrt-CI)，十分感谢！

使用的固件源码包括openwrt官方，以及coolsnowwolf、Lienol、immortalwrt、x-wrt维护的版本，详见[表格](#固件源码)。

预置机型有小米4A千兆版、小米3Gv2、小米CR6606、小米CR6608、小米CR6609等，详见[表格](#各机型对应文件)。

**快速生成固件 ---> 登陆GitHub，fork此仓库，点击上方`Actions`，选择左侧流程中的`build XXX`运行，运行完毕即可下载固件。示意如下：**

<img src="extra-files/images/action_running.gif" width="70%" ></img>

选择机型：在run workflow界面点开`选择设备`的下拉框，即可手动选择机型。

如预置机型中没有你需要的，可以使用[templet](templet)目录下的文件新增机型。

喜欢的话，右上角Star一下，方便再找。

## 使用本项目你需要

- GitHub 账号

- GitHub Actions 基本使用技能

**若要高度定制固件，需要掌握一定的Liunx、OpenWrt、[Actions](https://docs.github.com/cn/actions)等相关知识，途径：自行搜索学习**

## 使用教程

<details>
  
  <summary>点击展开/关闭</summary>

### 1. 注册GitHub账号并开启GitHub Actions

### 2. fork [hugcabbage/shared-lede](https://github.com/hugcabbage/shared-lede)

### 3. 自定义固件

什么也不修改，按默认配置，可以跳过此步。

每个机型关联三个文件，在preset-xxx目录中。

- [数字].clone.sh

此脚本用来拉取固件源码和扩展插件源码，新增插件源时，建议先在本地测试下是否缺依赖。

常用的克隆命令如下（克隆理解为下载即可）：

`git clone 链接`

`git clone -b 分支名 链接`

- [数字].modify.sh

此脚本用于固件初始化设置，修改登录IP、主机名、WiFi名称等。

此脚本用到最多的命令是sed，详细用法参见[链接](https://www.runoob.com/linux/linux-comm-sed.html)，这里只简单说明。

比如，下面这条命令就是用来修改管理IP的：

`sed -i 's/192.168.1.1/192.168.31.1/g' package/base-files/files/bin/config_generate`

`192.168.1.1`是源码中默认的lan口登录IP，也即初始的；`192.168.31.1`是新的，用来替换初始文本的。

可以看出命令的构成是这样的：

`sed -i 's/原字符串/新字符串/g' 文件路径`

这就可以用来替换掉源码中的特定位置，-i指直接改动文件，s指替换，g指全局。

原字符串记为str1，新字符串记为str2，自定义设置改动str2位置即可，如果你改动了str1，那么命令在源码中就匹配不到东西了，替换也就无效了。

>🎈🎈🎈 各基础命令的用法可参考该[链接](https://github.com/danshui-git/shuoming/blob/master/ming.md)，适合新手查阅。

- [数字].config

该文件对应本地编译执行make menuconfig后生成的.config文件。

该文件主要包含luci应用，流程中会自动转为完整的.config。

增减插件修改这个文件即可，以argon主题为例，格式如下：

 `CONFIG_PACKAGE_luci-theme-argon=y`   选中编译进固件的是这种

 `CONFIG_PACKAGE_luci-theme-argon=m`   选中仅编译ipk插件是这种

 `# CONFIG_PACKAGE_luci-theme-argon is not set`  未选中是这种

### 4. Actions中手动开始编译流程

选择你需要的`build XXX`workflow，再点击`Run workflow`，按需填内容，运行即可。

各选项说明如下:

- 超频到1100Mhz:

仅`build lede`有此选项。

默认不勾选。仅适用于5.10内核，除红米AX6S外，其余机型默认皆为5.10内核。

- 使用5.15内核:

仅`build lede`有此选项。

默认不勾选。lean lede源码勾选此项时，编译小米4A千兆版和小米3Gv2时会报错，勿用。

红米AX6S只有5.15内核，不必勾选。

- 选择机型:

点开下拉框，可以选择不同的机型。

- 上传到release:

默认勾选。单文件不能超过2GB，可添加内容记录。 release区见下图：

<img src="extra-files/images/release_zone.png" width="70%" ></img>

- 上传到artifact:

默认不勾选。artifact区见下图：

<img src="extra-files/images/artifact_zone.png" width="70%" ></img>

- 版本描述:

可作一些简单记录，会在release中显示。

### 5. 编译完成

Actions流程顺利完成后，去release(或者artifact)下载你的固件，release中allfiles.zip是所有文件的打包。

</details>

## 固件源码

|配置目录|流程名|源码|
|:----:|:----:|:----:|
|preset-lede|build lede|[coolsnowwolf/lede](https://github.com/coolsnowwolf/lede)|
|preset-lienol-openwrt|build lienol openwrt|[Lienol/openwrt master](https://github.com/Lienol/openwrt/tree/master)|
|preset-openwrt|build openwrt 23.05|[openwrt/openwrt openwrt-23.05](https://github.com/openwrt/openwrt/tree/openwrt-23.05)|
|preset-immortalwrt|build immortalwrt 21.02|[immortalwrt/immortalwrt openwrt-21.02](https://github.com/immortalwrt/immortalwrt/tree/openwrt-21.02)|
|preset-x-wrt|build x-wrt|[x-wrt/x-wrt master](https://github.com/x-wrt/x-wrt/tree/master)|

## 各机型对应文件

<table>
<thead>
  <tr>
    <th>机型</th>
    <th>配置目录下的关联文件</th>
  </tr>
</thead>
<tbody align="center">
  <tr>
    <td>小米4</td>
    <td rowspan="9">1.config<br>1.clone.sh<br>1.modify.sh</td>
  </tr>
  <tr>
    <td>小米3G</td>
  </tr>
  <tr>
    <td>小米3Pro</td>
  </tr>
  <tr>
    <td>小米CR6606</td>
  </tr>
  <tr>
    <td>小米CR6608</td>
  </tr>
  <tr>
    <td>小米CR6609</td>
  </tr>
  <tr>
    <td>红米AC2100</td>
  </tr>
  <tr>
    <td>小米AC2100</td>
  </tr>
  <tr>
    <td>红米AX6S</td>
  </tr>
  <tr>
    <td>斐讯K2P</td>
    <td rowspan="11">2.config<br>1.clone.sh<br>1.modify.sh</td>
  </tr>
  <tr>
    <td>小米3Gv2</td>
  </tr>
  <tr>
    <td>小米4A千兆版</td>
  </tr>
  <tr>
    <td>小米4A千兆版v2</td>
  </tr>
  <tr>
    <td>小米4A百兆版</td>
  </tr>
  <tr>
    <td>小米4C</td>
  </tr>
  <tr>
    <td>小米WiFi R3</td>
  </tr>
  <tr>
    <td>小米WiFi nano</td>
  </tr>
  <tr>
    <td>小米WiFi mini</td>
  </tr>
  <tr>
    <td>GL.iNet mt300n v2</td>
  </tr>
  <tr>
    <td>GL.iNet microuter n300</td>
  </tr>
</tbody>
</table>

## 提示

1. 直接在Actions中运行`build XXX`就能编译出固件，但默认插件数量较少，对插件有增、减需要的，到`[数字].config`中自行选择。若在`[数字].clone.sh`中添加了插件源，在`[数字].config`要作对应修改，建议先在本地make menuconfig测试。

1. 超频方案默认不启用，方案来自该[帖子](https://www.right.com.cn/forum/thread-4042045-1-1.html)。

1. 小米4A千兆版和小米3Gv2需修改分区才能在breed直刷，参考该[帖子](https://www.right.com.cn/forum/thread-4052254-1-1.html)，本项目中已修改好，见脚本[modify-xiaomi-router-4a-3g-v2.sh](extra-files/modify-xiaomi-router-4a-3g-v2.sh)。

1. 小米4A千兆版和小米3Gv2闪存小(仅16MB)，若编译插件太多，包体积超出闪存上限，则不会生成sysupgrade.bin。

---

## 最后

无特别详细的教程，自己摸索吧。

如有问题，请利用庞大的网络知识库，能快速解决你的问题。
