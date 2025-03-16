class Config:
    SECRET_KEY = 'ZHAOYAN'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lab.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True  # 仅HTTPS传输Cookie