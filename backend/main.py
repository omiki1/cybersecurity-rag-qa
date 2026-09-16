from fastapi import FastAPI

# 启动项目和关闭项目分别执行一些内容
from contextlib import asynccontextmanager

from auth.controller.AuthController import auth_router
from chat.controller.ChatController import chat_router
from chat.controller.HistoryController import history_router
from user.controller.UserController import users_router


@asynccontextmanager
async def start_end_run(app):
    """
        app：FastAPI 对象
        yield 之前的内容：启动项目执行
        yield 之后的内容：关闭项目执行
        如果想实现一些变量的初始化操作，可以把变量写入到 app.state 属性中，格式如下：
            app.state.变量名 = 初始化值
        如果某个接口中需要使用，就用 request 对象取出来，格式如下
            变量名2 = request.app.state.变量名
    """
    # app.state.username = "cc"
    print("启动项目")
    _prewarm()
    yield
    print("关闭项目")

# 创建FastAPI对象
app = FastAPI(lifespan=start_end_run)

# 导入子路由对象

# 注册子路由
app.include_router(
    router=auth_router,  # 引入子路由对象
    prefix="/auth",  # 配置访问子路由接口的前缀，默认""，推荐写为模块的包名做区分
    tags=['auth'],  # 配置swaggerUI中的模块名称
)

app.include_router(
    router=users_router,  # 用户模块路由
    prefix="/users",  # 访问前缀 /users
    tags=['user'],  # swaggerUI 模块名
)
app.include_router(
    router=chat_router,  # 用户模块路由
    prefix="/chat",  # 访问前缀 /users
    tags=['chat'],  # swaggerUI 模块名
)
app.include_router(
    router=history_router, prefix="/history", tags=['history'],
)
# 静态资源配置
from fastapi.staticfiles import StaticFiles

app.mount(
    "/static",  # 静态资源访问前缀 --- 请求路径
    StaticFiles(directory="static"),  # 静态资源目录 --- 放行文件夹
    name="static",  # 静态资源访问的模块名称
)

# 跨域配置（必须放在启动块之前，否则不生效）
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_origins=["http://localhost:8080"],  # 前端 Vite 端口
    allow_headers=["*"],
)
def _prewarm():
    import time
    time_start = time.time()
    from rag.VectorRetriever import load
    from rag.BM25Retriever import get_bm25_index
    load()
    docs,bm25_index = get_bm25_index(load())
    print(f'BM25 索引完成，共 {len(docs)} 条文档')
    print(f'预热完成，总耗时 {time.time() - time_start:.1f}s')






# 启动服务
if __name__ == '__main__':
    # 导入uvicorn包来写命令启动fastapi服务器项目
    import uvicorn as uv

    # 配置启动
    uv.run(
        # 启动项目的文件，即FastAPI()对象所在的文件
        app="main:app",  # 配置启动的项目文件 --- main.py中的app对象
        host="localhost",  # 配置启动的服务器地址
        port=8000,  # 配置启动的服务器端口
        reload=False,  # 配置关闭自动重启
    )
