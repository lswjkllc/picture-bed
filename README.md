# picture-bed
用于存放图片，俗称“图床”

# 功能
1、支持['jpg', 'jpeg', 'gif', 'png']四种图片类型上传功能
2、不支持重复上传，不同名
3、支持图片获取

# sample
上传图片
```angular2html
curl http://__DOMAIN__/api/upimg -F "file=@__UPFILE_PATH__" -H "token: __TOKEN__" -v
```
* __DOMAIN__ 表示域名，如果没有域名，直接填 **服务器地址+端口号**
* __UPFILE_PATH__ 表示需要上传的文件路径
* __TOKEN__ 表示服务器权限，俗称通行令

获取图片
```angular2html
http://localhost:8000/api/img?path=d4/f187d215e76cef045d5901a640c447.png
```
