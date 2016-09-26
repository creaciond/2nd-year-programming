def main():
    countries = {'Испания':['Мадрид', 46.77]}
    cntrs = countries.keys()
    for each in cntrs:
        values = countries.getvalues(each)
        print('Страна: %s, столица: %s, население: %d'% each,countries[each])

if __name__ == '__main__':
    main()
