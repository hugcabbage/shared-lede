# 使用 GitHub Actions 快速定制编译 OpenWrt 固件

流程文档参考[KFERMercer/OpenWrt-CI](https://github.com/KFERMercer/OpenWrt-CI)，十分感谢！

预置机型小米4A千兆版、小米CR6608、红米AC2100，默认编译小米4A千兆版。

需要其他机型可参考以上，并修改templet目录下的各文件，以作新增机型，[使用教程](templet/instruction.md)。

喜欢的话，Star一下，方便再找。

## 使用本项目你需要:

- GitHub 账号

- GitHub Actions 基本使用技能

#### 若要高度定制固件，需要掌握一定的Liunx、OpenWrt、[Actions](https://docs.github.com/cn/actions)等相关知识，途径：自行搜索学习

## 使用教程:

### 1. 注册GitHub账号并开启GitHub Actions

### 2. fork [hugcabbage/shared-lede](https://github.com/hugcabbage/shared-lede)

### 3. 设置Actions secrets

只上传到artifact，可以跳过此步。

进入GitHub Settings(点头像) → Developer settings → Personal access tokens → Generate new token，Note随意填，Expiration建议选`No expiration`，Select scopes里勾选`repo`、`workflow`，点Generate token，复制下长串token。

进入你fork的项目shared-lede下，点Settings → Secrets → Actions → New repository secret，Name填`RELEASE_FIRMWARE`，Value填复制的token，点Add secret。

### 4. 自定义固件

以小米4A千兆版为例，主要修改四个文件，在preset-models目录中。

> `1clone.sh`

固件源码和插件源码，新增插件源时，建议先在本地测试下是否缺依赖。

> `1modify.sh`

固件初始化设置，修改登录IP、主机名、WiFi名称等。

> `1.config`

只带luci应用、theme这两部分，流程中会转为.config，并自动补全为完整的。

> `release_content.txt`

此文本仅作release记录，其中的IP、密码与固件并无关联，怎么改都可以。

### 5. Actions中手动开始编译流程

选择你的`Workflow`，点击Run workflow，按需填内容，运行即可。

对部分选项说明一下

> 上传到release: 

默认勾选。推荐，空间无限，单文件不能超过2GB，有内容记录。

> 上传到artifact: 

默认不勾选。不推荐，无内容记录。

> 版本描述: 

可作一些简单记录，会在release中显示。

### 6. 编译完成

Actions流程顺利完成后，去release(或者artifact)下载你的固件，allfiles.zip是所有文件的打包。

## 关于小米4A千兆版

1.创建好secret后，直接运行`Workflow`就能编译出固件。默认插件数量较少，对插件有增、减需要的，到`1.config`中自行选择。若在`1clone.sh`中添加了插件源，在`1.config`要作对应修改，建议先在本地make menuconfig测试。

2.该机型需修改分区才能在breed直刷，参考[帖子](https://www.right.com.cn/forum/thread-4052254-1-1.html)，本项目中已修改好。

3.带超频方案，默认不启用，方案来自[帖子](https://www.right.com.cn/forum/thread-4042045-1-1.html)。

4.该机型闪存小，若编译插件太多，包体积超出16064K，则不会生成sysupgrade.bin。<br/>
可以去[官方插件库](https://downloads.openwrt.org/snapshots/packages/mips_24kc/packages/)参考各插件大小，下方也列出了几个较大插件的最近版本的体积:<br/>
UnblockNeteaseMusic-Go_0.2.13 --- 2.05MB<br/>
luci-app-openclash_0.44.16 --- 2.14MB<br/>
luci-app-vssr_1.23 --- 2.87MB<br/>
xray-core_1.5.3 --- 5.63MB<br/>

---

## 最后

不准备出什么详细的教程，自己摸索吧。

如有问题，请利用庞大的网络知识库，能快速解决你的问题。
