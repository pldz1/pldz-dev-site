import os
import sys
import dotenv

DEFAULT_RESOURCE_PATH = "data/resources"
DEFAULT_IMAGE_PATH = "data/images"
DEFAULT_ARTICLES_PATH = "data/articles"
DEFAULT_CACHE_PATH = "data/cache"
DEFAULT_WEBP_CACHE_PATH = "data/webp"
DEFAULT_DB_PATH = "data/db"
DEFAULT_WWW_PATH = "data/www"


class ProjectConfig:
    '''
    整个项目的配置文件
    '''
    # 当前文件相对于项目main.py的层级
    DIR_LOOP = 2

    PROJECT_ROOT = ''

    @classmethod
    def load_env(cls) -> None:
        """
        加载环境变量文件 .env
        """

        # 确定项目根目录
        cls.PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        for _ in range(ProjectConfig.DIR_LOOP):
            cls.PROJECT_ROOT = os.path.dirname(cls.PROJECT_ROOT)

        # 判断环境文件是否存在
        env_file_path = cls.get_abs_path('', '.env')
        if not os.path.exists(env_file_path):
            print(f"环境变量文件 .env 未找到: {env_file_path}")
            sys.exit(1)

        # 加载环境变量
        dotenv.load_dotenv(env_file_path, override=False)

    @classmethod
    def get_abs_path(cls, folder: str = None, fileName: str = None, file_name: str = None) -> str:
        '''
        获取任何项目文件的绝对路径
        '''
        folder = folder if folder is not None else ''
        file_name = file_name if file_name is not None else fileName
        file_name = file_name if file_name is not None else ''
        path = os.path.normpath(os.path.join(cls.PROJECT_ROOT, folder, file_name))
        return path

    @classmethod
    def get_statics_path(cls) -> str:
        '''
        获得静态资源的绝对路径
        '''
        return cls.get_abs_path('server/statics')

    @classmethod
    def get_resource_path(cls) -> str:
        '''
        获得资源文件的绝对路径
        '''
        resources_path = os.environ.get('RESOURCES_PATH', DEFAULT_RESOURCE_PATH)
        return cls.get_abs_path(resources_path)

    @classmethod
    def get_images_path(cls) -> str:
        '''
        获得存储图像的绝对路径
        '''
        image_path = os.environ.get('IMAGES_PATH', DEFAULT_IMAGE_PATH)
        return cls.get_abs_path(image_path)

    @classmethod
    def get_articles_path(cls) -> str:
        '''
        获得存储文章的绝对路径
        '''
        articles_path = os.environ.get('ARTICLES_PATH', DEFAULT_ARTICLES_PATH)
        return cls.get_abs_path(articles_path)

    @classmethod
    def get_cache_path(cls) -> str:
        """
        获取缓存目录的路径
        """
        cache_path = os.environ.get('CACHE_PATH', DEFAULT_CACHE_PATH)
        return cls.get_abs_path(cache_path)

    @classmethod
    def get_webp_cache_path(cls) -> str:
        """
        获取缓存目录的路径
        """
        webp_cache_path = os.environ.get('WEBP_CACHE_PATH', DEFAULT_WEBP_CACHE_PATH)
        return cls.get_abs_path(webp_cache_path)

    @classmethod
    def get_livedemo_config_path(cls) -> str:
        """
        获取livedemo配置的json文件
        """
        resource_path = cls.get_resource_path()
        return os.path.join(resource_path, 'website/livedemo.json')

    @classmethod
    def get_db_path(cls) -> str:
        """
        获取 JSON 数据库文件目录的绝对路径
        """
        db_path = os.environ.get('DB_PATH', DEFAULT_DB_PATH)
        return cls.get_abs_path(db_path)

    @classmethod
    def get_www_path(cls) -> str:
        """
        Get the directory that stores static site deployments.
        """
        www_path = os.environ.get('WWW_PATH', DEFAULT_WWW_PATH)
        return cls.get_abs_path(www_path)
