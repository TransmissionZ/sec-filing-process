INPUT_FOLDER_NAME = "CIK/"


import re
import os
import xml.etree.ElementTree as ET
from lxml import etree
from io import StringIO
from bs4 import BeautifulSoup as soup
import csv



class Parser:
    def __init__(self, input_folder):
        self.extracted = False
        self.input_folder = input_folder
        return

    def listdir(self, location):
        return os.listdir(self.input_folder + location + "/")

    def getpath(self, location, t):
        return os.path.join(self.input_folder, location, t)

    def parse(self):
        c = 0
        with open('employee_file.csv', mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(["CIK", "Filed As Of Date", "Conformed Period Of Report", "Employees"])
            l = len(os.listdir(self.input_folder))
            for p in os.listdir(self.input_folder):
                c += 1
                if len(self.listdir(p)) == 0:
                    continue
                for t in (self.listdir(p)):
                    try:
                        self.extract(p, t, employee_writer)
                    except Exception as e:
                        print(e)
                if (c % 10 == 0):
                    print("CIK's Done: " + str(c) + "/" + str(l))

    def searchstyle(self, tag):
        import re
        tag_style = tag.attrs.get('style')
        return bool(re.search(r'FONT-FAMILY.*:[^:]Times New Roman*', tag_style)) if tag_style else False

    def extract(self, p, t, employee_writer):
        employees = ""
        with open(self.getpath(p, t), 'r') as f:
            lines = f.readlines()
            for l in lines:
                if ("central index key:" in l.lower()):
                    n = l.find(":")
                    cik = l[n+1:].strip()
                if ("conformed period of report:" in l.lower()):
                    n = l.find(":")
                    cpor = l[n + 1:].strip()
                if ("filed as of date:" in l.lower()):
                    n = l.find(":")
                    faod = l[n + 1:].strip()
            try:
                # print(p + "/" + t)
                f.seek(0)
                file = f.read()
                n = [m.start() for m in re.finditer("<html>", file, re.IGNORECASE)] # file.lower().find("<html>")
                n1 = [m.end() for m in re.finditer("</html>", file, re.IGNORECASE)] # file.lower().find("</html>")
                # file = file[n[0]:n1[0]]

                for nn, nn1 in zip(n, n1):
                    file = file[nn:nn1]
                    found = False
                    for match in (re.finditer(r"(>\s*\S*\s*employees and Office Space\s*(</[a-zA-Z]*>)+)|(>\s*\S*\s*employees:?\s*(</[a-zA-Z]*>)+)|(>\s*\S*\s*employee relations:?\s*(</[a-zA-Z]*>)+)", file, flags=re.IGNORECASE)):
                        if "key" in match.group().lower():
                            continue
                        n2 = match.start()
                        file2 = file[n2:n2+2000]
                        s = soup(file2, 'lxml')
                        # print(s)
                        ps = s.findAll(re.compile(r'p|div'))
                        # print(ps)
                        # print(match.group())
                        for data in ps[1:]:
                            if not data.text or len(data.text) <= 30:
                                continue
                            else:
                                # print(match.group())
                                found = True
                                employees = data.text
                                break
                    if found:
                        break
            except Exception as e:
                print(p + "/" + t)
                print(e)
                employees = ""
            employees = employees.replace("\n", " ").replace("\t", " ").strip()
            if not employees:
                employees = ""
            # print(employees)
            employee_writer.writerow([cik, faod, cpor, employees])
            # print('\n')
            # s = soup(file, 'lxml')
            # ps = s.findAll('p')
            # for idx, ptag in enumerate(ps):
            #     if re.search(r">\s?Employees\s?<", str(ptag), flags=re.IGNORECASE):
            #         # print(ptag)
            #         print(idx)
            #         break
            # try:
            #     print(ps[idx].text.strip())
            #     idx += 1
            #     c = 0
            #     while (ps[idx].text.strip() == ""):
            #         idx += 1
            #
            #         c += 1
            #         if (c == 3):
            #             raise Exception
            #     print(idx)
            #     print(ps[idx].text.strip())
            # except Exception as e:
            #     print("ERRORRR" + str(c))
            #     # print(p + "/" + t)
            #     ps = s.findAll('div')
            #     print(len(ps))
            #     for idx, ptag in enumerate(ps):
            #         print(ptag)
            #         if re.search(r">Employees<", str(ptag)):
            #             idx2 = idx
            #             try:
            #                 idx2 += 1
            #                 c = 0
            #                 while (ps[idx2].text.strip() == ""):
            #                     idx2 += 1
            #                     c += 1
            #                     if (c == 3):
            #                         raise Exception
            #                 if ps[idx2].text.strip() == "":
            #                     continue
            #
            #             except Exception as e:
            #                 print(p + "/" + t)
            #                 print(e)

if __name__ == '__main__':
    p = Parser(INPUT_FOLDER_NAME)
    p.parse()
    # p.extract('17485', '0000950123-09-071527.txt')
    # p.extract('9892', '0001193125-09-039210.txt')
    # p.extract('4962', '0000004962-18-000032.txt')
    # p.extract('17843', '0001193125-08-183570.txt')
    # p.extract('19745', '0000950123-10-022158.txt')
    # p.extract('19745', '0000019745-07-000004.txt')
    # p.extract('7623', '0001437749-15-001434.txt')