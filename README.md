## Backend运行：

1.安装好所有需要的python包

2.terminal 命令（先进入back-end文件夹）：

python app.py

### Model:
inceptionv3_fcn_model.h5 must be placed in the `back-end` directory.
inceptionv3_fcn_model.h5 can be trained from InceptionV3_Model_v1.1.py

## Frontend运行：

terminal命令（先进入front-end文件夹）：：

npm install之后会自动出现node_modules文件夹，注意这一步有报错是非常正常的

npm run dev

## Inference:

Currently, a `smalldata_X_Y` file must be zipped and used as data to be analysed.