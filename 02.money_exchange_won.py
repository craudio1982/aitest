import sys


EXCHANGE_RATES = {
    "USD": 1340.0,
    "JPY": 9.2,
    "CNY": 184.0,
}


def get_exchange_rates():
    return EXCHANGE_RATES


def convert_won_to_currency(won_amount, currency_code):
    rate = get_exchange_rates()[currency_code.upper()]
    return round(won_amount / rate, 2)


def display_screen():
    print("=" * 50)
    print("            원화 환전 계산기")
    print("=" * 50)
    print("실시간 환율 확인이 가능한 간단한 화면입니다.")
    print("환율은 예시 기준이며, 실제 환율은 변동될 수 있습니다.")
    print()
    print("[환전 통화 선택]")
    print("1. USD(달러)")
    print("2. JPY(엔화)")
    print("3. CNY(위안화)")
    print("q. 종료")
    print("-" * 50)


def main():
    while True:
        display_screen()
        choice = input("선택하세요: ").strip().lower()

        if choice in {"q", "quit", "exit"}:
            print("프로그램을 종료합니다.")
            sys.exit(0)

        currency_map = {
            "1": ("USD", "달러"),
            "2": ("JPY", "엔화"),
            "3": ("CNY", "위안화"),
        }

        if choice not in currency_map:
            print("올바른 번호를 입력해 주세요.\n")
            continue

        currency_code, currency_name = currency_map[choice]

        try:
            won_amount = float(input("환전할 원화 금액을 입력하세요: "))
        except ValueError:
            print("숫자만 입력해 주세요.\n")
            continue

        if won_amount <= 0:
            print("0보다 큰 금액을 입력해 주세요.\n")
            continue

        converted_amount = convert_won_to_currency(won_amount, currency_code)
        print(f"\n결과: {won_amount:,.0f}원 -> {currency_name} {converted_amount:,.2f}")
        print("=" * 50)
        input("계속하려면 Enter를 누르세요...")
        print()


if __name__ == "__main__":
    main()
