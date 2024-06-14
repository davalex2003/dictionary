import PyPDF2 as pdf


def parse_pdf(pdf_file: str) -> list:
    dict_pdf = open(pdf_file, 'rb')
    pdf_reader = pdf.PdfReader(dict_pdf)
    pages_num = len(pdf_reader.pages)
    extracted_dict = []

    for page_num in range(pages_num):
        text = pdf_reader.pages[page_num].extract_text()

        # Убираем номер страницы
        text = text.replace(str(page_num + 1), '')

        # Убираем лишние переводы строки:
        text = text.replace('\n', '$')
        text = text.replace('. $', '\n')
        text = text.replace('$', '')

        # Убираем деффисы:
        text = text.replace('\xad', '')

        # Чтобы дальше убрать подсказку в самом начале
        index = text.index(' ')
        text = text[:index] + '\n' + text[index + 1:]

        lexemes = text.split('\n')
        lexemes.remove(lexemes[0])  # убираем подсказку

        # Убираем лишние записи:
        letters = [lexema[0] for lexema in lexemes]
        letter = max(set(letters), key=letters.count)

        lexemes_ = []
        for lexema in lexemes:
            if lexema[0] == letter:
                lexemes_.append(lexema)

        # Делим на слова и определения:
        lexemes = []
        for lexema in lexemes_:
            try:
                index = lexema.index(' ')
                lexemes.append([lexema[:index], lexema[index + 1:]])
            except ValueError:
                pass

        # Добавляем полученные пары "Лексема - Описание" в словарь
        for pair in lexemes:
            extracted_dict.append([pair[0], {'Definition': pair[1]}])

    dict_pdf.close()
    return extracted_dict
