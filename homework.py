######################################
class Tag:
    tag = ""
    tab = 0
    text = ""
    attributes = {}
    is_single = False
    childrens = []

    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.attributes = {}
        self.is_single = is_single
        self.childrens = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)
        for key, value in kwargs.items():
            self.attributes[key] = value
    
    def increseTab(self):
        for child in self.childrens:
            child.increseTab()
        self.tab += 1
        return self

    def __str__(self):
        # строка аттрибутов текущего тэга. Сначала пустая
        attrs = []
        # берем все аттрибуты какие есть в attributes и заталкиваем в строку attrs через " "
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = (" "+" ".join(attrs)) if len(attrs) else ""
        # смотрим есть ли вложенные тэги и если есть то пишем открывающий тэг и идем внутрь вложения
        if self.childrens:
            # получаем открывающий тэг и все аттрибуты с предцдущего шага 
            opening = self.tab *"  "+"<{tag}{attrs}>".format(tag=self.tag,  attrs=attrs)+"\n"
            # получаем текст тэга (то что между откр и закр) 
            internal = "%s" % self.text
            # ныряем во вложенные тэги и выводим их точно таким же способом
            for child in self.childrens:
                #ставим перевод строки и добавляем 4 отступа. надо подумать как сделать красиво
                internal +=str(child)
            # получаем закрывающий тэг
            ending =  self.tab *"  "+"</%s>" % self.tag
            # возвращаем строку со всем полученным содержимым
            return opening +internal +ending + "\n"
        # если вложеных тегов нет то 
        else:
            # если тег одинарный, то готовим его (тэг) и возвращаем в виде строки
            if self.is_single:
                return  self.tab *"  "+"<{tag}{attrs}/>\n".format(tag=self.tag, attrs=attrs)
            # если тег не одинарный но и без детей, то заполняем его по шаблону из полученных выше значений и возвращаем
            else:
                return  self.tab *"  "+"<{tag}{attrs}>{text}</{tag}>\n".format(
                    # коряво но думать уже нет сил
                    tag=self.tag,   attrs=attrs, text=self.text
                )

    def __iadd__(self, other):
        self.childrens.append(other)
        other.increseTab()
        return self

    def __enter__(self, **kwargs):
        return self

    def __exit__(self, type, value, traceback):
        pass
    pass
######################################
# class TopLevelTag(Tag):
# Отказался от класса так как не понял зачем он
######################################
# Класс HTML - потомок Tag который открывает файл и имеет возможность записи

class HTML(Tag):
    tag="html"
    def __init__(self, output=None, **kwargs):
        self.file = open(output,"w")  
        pass
    def __enter__(self,  output=None, **kwargs):
        return self
    def __exit__(self, type, value, traceback):
        self.file.write(self.__str__())
        return self
    pass




if __name__ == "__main__":
    with HTML(output="index.html") as doc:
        with Tag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with Tag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1
            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph
                with Tag("img", is_single=True, src="https://i.ytimg.com/vi/tQXiKay0Ie8/hqdefault.jpg") as img:
                    div += img
                body += div
            doc += body
#вывод в консоль что бы не бегать в файл каждый раз для проверки
print(doc)

