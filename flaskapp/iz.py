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
 cho = StringField('Введите уровень зашумления', validators = [DataRequired()])
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

import random
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import seaborn as sns

## функция для оброботки изображения 

def draw1(filename,cho):
##открываем изображение 
 print(filename)
 img= Image.open(filename)
 draw = ImageDraw.Draw(img) #Создаем инструмент для рисования.
 width = img.size[0] #Определяем ширину. 
 height = img.size[1] #Определяем высоту. 
 pix = img.load() #Выгружаем значения пикселей.
 cho=int(cho)
	 
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
   rand = random.randint(-cho, cho)
   a = pix[i, j][0] + rand
   b = pix[i, j][1] + rand
   c = pix[i, j][2] + rand
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
  	
 output_filename = filename
 img.save(output_filename)
	
 
 return output_filename,gr_path

def draw2():
 img= Image.open(output_filename)
 ##делаем график
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path = "./static/newgr1.png"
 sns.displot(data)
 #plt.show()
 plt.savefig(gr_path)
 plt.close()
	
 return gr_path

# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные передаваемые в форму
 filename=None
 newfilename=None
 grname=None
 grname1=None
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  # файлы с изображениями читаются из каталога static
  filename = os.path.join('./static', secure_filename(form.upload.data.filename))
  ch=form.cho.data
 
  form.upload.data.save(filename)
  newfilename,grname = draw1(filename,ch)
  newfilename,grname1 = draw2(output_filename)
 # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
 # сети если был нажат сабмит, либо передадим falsy значения
 
 return render_template('net.html',form=form,image_name=newfilename,gr_name=grname,gr_name1=grname1)


if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
