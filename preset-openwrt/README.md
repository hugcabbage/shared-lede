## 本地测试生成.config文件

> 以生成other.config为例，编译流程`build openwrt`中`other`机型对应当前的other.config。

1. 使用Codespace或本地环境，克隆本仓库，并进入仓库根目录。

   建议使用Codespace，只需要一个浏览器即可，且不会存在网络问题。


1. 运行以下命令，克隆openwrt源码。

    ```shell
    chmod +x extra-files/local-clone.sh
    chmod +x extra-files/simplify.py
    ./extra-files/local-clone.sh
    cd _test_code
    ```

1. （可选）从已有的.config修改。

     ```shell
     cp ../preset-openwrt/other.config .config
     ```

1. 运行以下命令，开始配置。

    ```shell
    make menuconfig
    ```

1. 配置完成后，_test_code目录里，也就是现在所在的目录下已生成.config文件。

1. （可选）简化一下.config文件，只保留常用的配置项，运行以下命令。

   ```shell
   ../extra-files/simplify.py .config
   ```

1. 将.config文件复制到本仓库的preset-openwrt目录下，运行以下命令。

   ```shell
   cp .config ../preset-openwrt/other.config
   ```

1. 提交到远程仓库，开始运行编译流程`build openwrt`，选择机型`other`。
