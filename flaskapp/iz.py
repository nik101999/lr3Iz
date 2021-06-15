from flask import Flask
app = Flask(__name__)
#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
 return " <html><head></head> <body> Hello World! </body></html>"

from flask import render_template
#наша новая функция сайта

# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
import wtforms
from wtforms import StringField, SubmitField, TextAreaField
# модули валидации полей формы
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google 
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeMTzEbAAAAAOVvop7U91SZcrnjgO03XRwXK3Sr'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeMTzEbAAAAAIXuQ-3CRSyM6jK0668PzXW4qKkV'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap(app)
# создаем форму для загрузки файла
class NetForm(FlaskForm):
 # поле для введения строки, валидируется наличием данных
 # валидатор проверяет введение данных после нажатия кнопки submit
 # и указывает пользователю ввести данные если они не введены
 # или неверны
 cho1 = StringField('Введите уровень зашумления r', validators = [DataRequired()])
 cho2 = StringField('Введите уровень зашумления g', validators = [DataRequired()])
 cho3 = StringField('Введите уровень зашумления b', validators = [DataRequired()])
 # поле загрузки файла
 # здесь валидатор укажет ввести правильные файлы
 upload = FileField('Загрузить картинку', validators=[
 FileRequired(),
 FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 # поле формы с capture
 recaptcha = RecaptchaField()
 #кнопка submit, для пользователя отображена как send
 submit = SubmitField('send')
# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os
import scipy.ndimage.filters as filt
import random
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import numpy as np
import argparse
## функция для оброботки изображения 

def draw1(filename,cho1,cho2,cho3):
##открываем изображение 

 #print(filename)
 img= Image.open(filename)

 do = filename
 do = "./static/do.png"
 img.save(do)

 draw = ImageDraw.Draw(img) #Создаем инструмент для рисования.
 width = img.size[0] #Определяем ширину. 
 height = img.size[1] #Определяем высоту. 
 pix = img.load() #Выгружаем значения пикселей.
 cho1=int(cho1)
 cho2=int(cho2)
 cho3=int(cho3)
	 
##делаем график
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path = "./static/newgr.png"
 sns.displot(data)
 #plt.show()
 plt.savefig(gr_path)
 plt.close()
 
 
##меняем шум
 for i in range(width):
  for j in range(height):
   rand1 = random.randint(-cho1, cho1)
   rand2 = random.randint(-cho2, cho2)
   rand3 = random.randint(-cho3, cho3)
   a = pix[i, j][0] + rand1
   b = pix[i, j][1] + rand2
   c = pix[i, j][2] + rand3
   if (a < 0):
    a = 0
   if (b < 0):
    b = 0
   if (c < 0):
    c = 0
   if (a > 255):
    a = 255
   if (b > 255):
    b = 255
   if (c > 255):
    c = 255
   draw.point((i, j), (a, b, c))
  	
 po = './static/po.png'
 img.save(po)
 
 sg = filename
 
 img = cv2.imread('./static/po.png')
 kernel = np.ones((3,3),np.float32)/9
 sg = cv2.filter2D(img,-1,kernel)
 cv2.imwrite('./static/sg.png', sg)
 sg = './static/sg.png'
 


 
 return po ,gr_path,do,sg



# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные передаваемые в форму
 filename=None
 po=None
 sg=None
 do=None
 grname=None
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  # файлы с изображениями читаются из каталога static
  filename = os.path.join('./static', secure_filename(form.upload.data.filename))
  ch1=form.cho1.data
  ch2=form.cho2.data
  ch3=form.cho3.data
 
  form.upload.data.save(filename)
  po,grname,do,sg = draw1(filename,ch1,ch2,ch3)
  
 # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
 # сети если был нажат сабмит, либо передадим falsy значения
 
 return render_template('net.html',form=form,image_name=po,gr_name=grname,image_name1=do,image_name2=sg)


if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
