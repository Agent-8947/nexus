# 前端 部署和编译

## 快速部署

前往[Release 页面](https://github.com/SheepChef/Abracadabra/releases/latest)下载 `fastdeploy_X.X.zip`

然后，将它解压到你网站的任意位置，也可以直接上传到静态容器中。

配置路由，即可得到一个与[项目 Demo](https://abra.js.org/)一模一样的页面。

若要自行编译或修改前端代码，请前往前端源代码仓库。

浏览器插件的源码同样在前端源代码仓库，位于 crx 分支。

## 编译前端页面

首先，前往[前端源码仓库](https://github.com/SheepChef/Abracadabra_demo)，拉取前端源码仓库的代码。

```sh
git clone https://github.com/SheepChef/Abracadabra_demo.git
```

然后，切换到主分支。

```sh
git checkout main
```

现在你可以开始编译了，你最少需要执行两个指令：

```sh
npm install

npm run build
```

构建生成的文件在 `./docs` 文件夹内。

## 编译浏览器插件

拉取仓库代码后，切换到 `crx` 分支。

```sh
git checkout crx
```

::: tip 无法切换分支？
确保在切换分支之前，你没有未保存的修改。
:::

下一步，安装依赖并编译。

```sh
npm install --legacy-peer-deps

npm run build
```

::: warning --legacy-peer-deps
你必须附加 `--legacy-peer-deps` 参数，否则依赖将无法正常安装。
:::

构建生成的文件在 `./dist` 文件夹内，也许会生成一个无用的 `.vite` 文件夹，删除即可。
