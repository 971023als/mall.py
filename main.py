import json

persons = []


def f_load():
    global persons
    try:
        with open('persons.json', 'r', encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)
    except FileNotFoundError:
        persons = []
        return persons
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as e:
        print(f"persons.json을 읽을 수 없습니다 ({e}). 원본을 보호하기 위해 변경 없이 종료합니다.")
        raise SystemExit(1)
    if not isinstance(data, list) or any(not isinstance(p, dict) for p in data):
        print("persons.json이 회원 목록(딕셔너리 리스트) 형식이 아닙니다. 원본을 보호하기 위해 변경 없이 종료합니다.")
        raise SystemExit(1)
    persons = data
    return persons


def f_save():
    with open('persons.json', 'w', encoding='utf-8') as outfile:
        json.dump(persons, outfile, ensure_ascii=False, indent=4)


def _update_grade(person):
    count = person.get('access_count', 0)
    if count >= 100:
        person['grade'] = 'VIP'
    elif count >= 30:
        person['grade'] = 'SILVER'
    else:
        person['grade'] = 'STANDARD'


def f_menu():
    print("--------------------------------------------")
    print("1. 회원 리스트  read")
    print("2. 회원 만들기  create")
    print("3. 회원 삭제    delete")
    print("4. 이름 -> 전화번호변경")
    print("5. 회원 분석")
    print("6. 회원 등급 확인")
    print("7. 종료")
    print("--------------------------------------------")
    while True:
        try:
            menu = int(input("메뉴를 선택하시오: "))
            if 1 <= menu <= 7:
                return menu
            print("1~7 사이의 숫자를 입력하세요.")
        except ValueError:
            print("입력값이 숫자가 아닙니다.")


def f_display():
    f_load()
    print("{:<12}\t| {:<15}| {:<5}| {}".format('이름', '전화번호', '나이', '취미'))
    print("------------------------------------------------")
    if len(persons) == 0:
        print('등록된 회원이 없습니다.')
        return
    for person in persons:
        print("{:<12}\t| {:<15}| {:<5}| {}".format(
            person['name'],
            person['phone'],
            str(person['age']),
            person['hobby']
        ))
        print("------------------------------------------------")


def f_input():
    name = input("이름을 입력하시오: ")
    phone = input("전화번호를 입력하세요: ")
    while True:
        try:
            age = int(input("나이를 입력하세요: "))
            break
        except ValueError:
            print("나이는 숫자로 입력하세요.")
    hobby = input("취미를 입력하세요: ")

    person = {
        'name': name,
        'phone': phone,
        'age': age,
        'hobby': hobby,
        'access_count': 0,
        'grade': 'STANDARD'
    }
    persons.append(person)
    f_save()
    print(f"'{name}' 회원이 등록되었습니다.")


def f_modify():
    f_load()
    old_name = input("변경하고 싶은 이름을 입력하시오: ")
    matches = [i for i, p in enumerate(persons) if p['name'] == old_name]

    if len(matches) == 0:
        print("이름이 발견되지 않았음")
        return

    if len(matches) > 1:
        print(f"동명이인이 {len(matches)}명 있습니다. 전화번호로 본인 확인합니다.")
        tel = input("전화번호를 입력하시오: ")
        matches = [i for i in matches if persons[i]['phone'] == tel]
        if len(matches) == 0:
            print("일치하는 회원이 없습니다.")
            return

    index = matches[0]
    new_phone = input("새로운 전화번호를 입력하시오: ")
    while True:
        try:
            new_age = int(input("새로운 나이를 입력하시오: "))
            break
        except ValueError:
            print("나이는 숫자로 입력하세요.")
    new_hobby = input("새로운 취미를 입력하시오: ")

    persons[index]['phone'] = new_phone
    persons[index]['age'] = new_age
    persons[index]['hobby'] = new_hobby
    f_save()
    print("수정이 완료되었습니다.")


def f_delete():
    f_load()
    del_name = input("삭제하고 싶은 이름을 입력하시오: ")
    matches = [i for i, p in enumerate(persons) if p['name'] == del_name]

    if len(matches) == 0:
        print("이름이 발견되지 않았음")
        return

    if len(matches) > 1:
        print(f"동명이인이 {len(matches)}명 있습니다. 전화번호로 본인 확인합니다.")
        del_tel = input("전화번호를 입력하시오: ")
        matches = [i for i, p in enumerate(persons) if p['name'] == del_name and p['phone'] == del_tel]
        if len(matches) == 0:
            print("일치하는 회원이 없습니다.")
            return

    persons.pop(matches[0])
    f_save()
    print(f"'{del_name}' 회원이 삭제되었습니다.")


def f_search():
    f_load()
    dic = {}
    for person in persons:
        hobby = person['hobby']
        dic[hobby] = dic.get(hobby, 0) + 1
    if not dic:
        print("등록된 회원이 없습니다.")
        return
    for key, value in dic.items():
        print(f"{key} {value}명")


def f_check():
    f_load()
    name = input("등급을 확인하고 싶은 회원의 이름을 입력하시오: ")
    found = False
    for person in persons:
        if person['name'] == name:
            person['access_count'] = person.get('access_count', 0) + 1
            _update_grade(person)
            print(f"{person['name']}님의 회원등급은 {person['grade']} 입니다.")
            found = True
    if found:
        f_save()
    else:
        print("해당 이름의 회원이 없습니다.")


if __name__ == '__main__':
    f_load()
    while True:
        menu = f_menu()
        if menu == 1:
            f_display()
        elif menu == 2:
            f_input()
        elif menu == 3:
            f_delete()
        elif menu == 4:
            f_modify()
        elif menu == 5:
            f_search()
        elif menu == 6:
            f_check()
        elif menu == 7:
            break
