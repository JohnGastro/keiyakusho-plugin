#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py - Utility Functions for Rabinet Contract Processing

ラビーネット契約書スキル用の共通ユーティリティ関数群
"""

import re
from datetime import datetime
from typing import Optional, Dict, List, Tuple


class DateConverter:
    """日付変換ユーティリティ"""

    @staticmethod
    def to_japanese_format(date_input, format_type='reiwa'):
        """
        日付を日本語形式に変換

        Args:
            date_input: datetime, 'YYYY-MM-DD', 'YYYY/MM/DD' など
            format_type: 'reiwa' (令和X年X月X日), 'heisei' (平成X年X月X日), 'slash' (R06/3/1)

        Returns:
            str: 日本語形式の日付
        """
        if isinstance(date_input, str):
            # 複数のフォーマットに対応
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d']:
                try:
                    date_input = datetime.strptime(date_input, fmt)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"サポートされていない日付フォーマット: {date_input}")

        if not isinstance(date_input, datetime):
            raise TypeError(f"日付型が不正: {type(date_input)}")

        year = date_input.year
        month = date_input.month
        day = date_input.day

        if format_type == 'reiwa':
            if year >= 2019:
                reiwa_year = year - 2018
                return f"令和{reiwa_year}年{month}月{day}日"
            elif year >= 1989:
                heisei_year = year - 1988
                return f"平成{heisei_year}年{month}月{day}日"
            else:
                return f"{year}年{month}月{day}日"

        elif format_type == 'heisei':
            if year >= 1989:
                heisei_year = year - 1988
                return f"平成{heisei_year}年{month}月{day}日"
            else:
                raise ValueError("平成形式は1989年以降に対応")

        elif format_type == 'slash':
            if year >= 2019:
                reiwa_year = year - 2018
                return f"R{reiwa_year:02d}/{month}/{day}"
            elif year >= 1989:
                heisei_year = year - 1988
                return f"H{heisei_year:02d}/{month}/{day}"
            else:
                return f"{year}/{month}/{day}"

        else:
            raise ValueError(f"サポートされていない形式タイプ: {format_type}")

    @staticmethod
    def parse_japanese_date(date_str):
        """
        日本語形式の日付文字列をdatetimeに変換

        Args:
            date_str: 令和X年X月X日 など

        Returns:
            datetime: パース済みの日時
        """
        # 令和XX年YY月ZZ日 -> YYYY-MM-DD
        patterns = [
            (r'令和(\d+)年(\d+)月(\d+)日', 2018),  # 令和 = 2018 + n
            (r'平成(\d+)年(\d+)月(\d+)日', 1988),  # 平成 = 1988 + n
            (r'(\d{4})年(\d+)月(\d+)日', None),     # YYYY年MM月DD日
        ]

        for pattern, base_year in patterns:
            match = re.match(pattern, date_str)
            if match:
                year_val, month, day = match.groups()
                year = int(year_val) + base_year if base_year else int(year_val)
                return datetime(year, int(month), int(day))

        raise ValueError(f"パースできない日付形式: {date_str}")


class CurrencyFormatter:
    """通貨フォーマットユーティリティ"""

    @staticmethod
    def to_format(value, separator=',', remove_unit=True):
        """
        数値を通貨形式に変換

        Args:
            value: 数値
            separator: 区切り文字（通常は',' または ''）
            remove_unit: 単位記号を除去するか

        Returns:
            str: フォーマット済み文字列
        """
        try:
            # 既存の区切りを削除
            if isinstance(value, str):
                value = value.replace(',', '').replace('万', '').replace('円', '').strip()
                value = float(value)
            else:
                value = float(value)

            # フォーマット
            return f"{int(value):,}".replace(',', separator)
        except (ValueError, TypeError) as e:
            raise ValueError(f"通貨フォーマットに失敗: {str(e)}")

    @staticmethod
    def to_man(value):
        """
        数値を万円単位で表記

        Args:
            value: 数値

        Returns:
            str: 万円単位の文字列（例: '3000万円'）
        """
        try:
            if isinstance(value, str):
                value = float(value.replace(',', ''))
            else:
                value = float(value)

            man = value / 10_000_000
            if man == int(man):
                return f"{int(man)}千万円" if man >= 1000 else f"{int(man)}万円"
            else:
                return f"{man:.1f}万円"
        except (ValueError, TypeError) as e:
            raise ValueError(f"万円変換に失敗: {str(e)}")


class ContractCalculator:
    """契約計算ユーティリティ"""

    @staticmethod
    def calculate_stamp_duty(contract_amount):
        """
        印紙税を計算

        Args:
            contract_amount: 売買代金または賃料

        Returns:
            int: 印紙税額（円）

        注: 2024年時点の税率。最新情報は国税庁を確認
        """
        amount = float(contract_amount)

        if amount < 10_000:
            return 0
        elif amount < 100_000:
            return 200
        elif amount < 1_000_000:
            return 200
        elif amount < 10_000_000:
            return 1_000
        elif amount < 50_000_000:
            return 10_000
        elif amount < 100_000_000:
            return 20_000
        elif amount < 500_000_000:
            return 60_000
        else:
            return 100_000

    @staticmethod
    def calculate_brokerage_fee(transaction_amount, with_tax=True, tax_rate=0.10):
        """
        仲介手数料を計算（標準額）

        Args:
            transaction_amount: 取引額
            with_tax: 消費税を含めるか
            tax_rate: 消費税率（デフォルト10%）

        Returns:
            dict: {'base': 基本額, 'tax': 消費税, 'total': 合計}
        """
        amount = float(transaction_amount)

        # 標準額計算（税抜）
        if amount <= 2_000_000:
            base = int(amount * 0.05)
        elif amount <= 4_000_000:
            base = int(2_000_000 * 0.05 + (amount - 2_000_000) * 0.04)
        else:
            base = int(2_000_000 * 0.05 + 2_000_000 * 0.04 + (amount - 4_000_000) * 0.03)

        tax = int(base * tax_rate) if with_tax else 0
        total = base + tax

        return {
            'base': base,
            'tax': tax,
            'total': total,
            'description': f"{base:,}円 + 消費税 {tax:,}円 = {total:,}円" if with_tax else f"{base:,}円"
        }

    @staticmethod
    def calculate_remaining_price(total_price, deposit):
        """
        残代金を計算

        Args:
            total_price: 売買代金総額
            deposit: 手付金

        Returns:
            int: 残代金
        """
        return int(float(total_price) - float(deposit))


class AddressNormalizer:
    """住所正規化ユーティリティ"""

    @staticmethod
    def normalize(address: str) -> str:
        """
        住所を正規化（全角・半角統一、改行除去など）

        Args:
            address: 住所文字列

        Returns:
            str: 正規化済み住所
        """
        # 改行を削除
        address = address.replace('\n', '').replace('\r', '')

        # 複数スペースを単一スペースに
        address = re.sub(r'\s+', ' ', address)

        # 前後の空白を削除
        address = address.strip()

        return address

    @staticmethod
    def split_address(address: str) -> Dict[str, str]:
        """
        住所を都道府県、市区町村、それ以降に分割

        Args:
            address: 住所文字列

        Returns:
            dict: {'prefecture': '東京都', 'city': '渋谷区', 'detail': '道玄坂1-1'}

        注: 簡易的な分割のみ
        """
        # 都道府県一覧
        prefectures = [
            '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
            '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
            '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県',
            '岐阜県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
            '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
            '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県',
            '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'
        ]

        address = address.strip()
        prefecture = ''
        remaining = address

        for pref in prefectures:
            if address.startswith(pref):
                prefecture = pref
                remaining = address[len(pref):]
                break

        # 市区町村の簡易抽出（最初の2～4文字）
        city_match = re.match(r'([^\d]*[市区町村])', remaining)
        city = city_match.group(1) if city_match else ''
        detail = remaining[len(city):].lstrip() if city else remaining

        return {
            'prefecture': prefecture,
            'city': city,
            'detail': detail,
            'full': address
        }


class NameValidator:
    """名前検証ユーティリティ"""

    @staticmethod
    def validate_person_name(name: str) -> Tuple[bool, str]:
        """
        個人名の妥当性をチェック

        Args:
            name: 人名

        Returns:
            (bool, str): (妥当か, メッセージ)
        """
        name = name.strip()

        if not name:
            return False, "名前が空です"

        if len(name) < 2:
            return False, "名前は2文字以上必要です"

        if len(name) > 50:
            return False, "名前が長すぎます（50文字以内）"

        # 基本的な文字チェック（禁止文字）
        invalid_chars = ['<', '>', '"', "'", '&', '%', '$', '#', '@']
        if any(char in name for char in invalid_chars):
            return False, f"使用できない文字が含まれています"

        return True, "OK"

    @staticmethod
    def validate_company_name(name: str) -> Tuple[bool, str]:
        """
        法人名の妥当性をチェック

        Args:
            name: 法人名

        Returns:
            (bool, str): (妥当か, メッセージ)
        """
        name = name.strip()

        if not name:
            return False, "法人名が空です"

        if len(name) < 3:
            return False, "法人名は3文字以上必要です"

        if len(name) > 100:
            return False, "法人名が長すぎます（100文字以内）"

        return True, "OK"


class AreaCalculator:
    """面積計算ユーティリティ"""

    @staticmethod
    def convert_area(value, from_unit, to_unit='m2'):
        """
        面積単位を変換

        Args:
            value: 数値
            from_unit: 元の単位 ('m2', 'tsubo', 'hectare')
            to_unit: 変換先単位

        Returns:
            float: 変換後の値
        """
        # m2を基準に変換
        to_m2_ratio = {
            'm2': 1,
            'tsubo': 3.30579,  # 1坪 ≈ 3.30579 m²
            'hectare': 10000,   # 1ヘクタール = 10000 m²
        }

        if from_unit not in to_m2_ratio:
            raise ValueError(f"未対応の単位: {from_unit}")
        if to_unit not in to_m2_ratio:
            raise ValueError(f"未対応の単位: {to_unit}")

        value_in_m2 = float(value) * to_m2_ratio[from_unit]
        return value_in_m2 / to_m2_ratio[to_unit]

    @staticmethod
    def format_area(value, unit='m2', precision=2):
        """
        面積をフォーマット

        Args:
            value: 数値
            unit: 単位
            precision: 小数点以下の桁数

        Returns:
            str: フォーマット済みの文字列
        """
        if unit == 'tsubo':
            return f"{float(value):.{precision}f}坪"
        elif unit == 'hectare':
            return f"{float(value):.{precision}f}ha"
        else:
            return f"{float(value):.{precision}f}㎡"


# 使用例とテスト
if __name__ == '__main__':
    # 日付変換テスト
    print("=== 日付変換テスト ===")
    dc = DateConverter()
    print(dc.to_japanese_format('2025-03-01', 'reiwa'))
    print(dc.to_japanese_format('2024-04-01', 'slash'))

    # 通貨フォーマットテスト
    print("\n=== 通貨フォーマットテスト ===")
    cf = CurrencyFormatter()
    print(cf.to_format(30000000))
    print(cf.to_man(30000000))

    # 契約計算テスト
    print("\n=== 契約計算テスト ===")
    calc = ContractCalculator()
    print(f"印紙税: {calc.calculate_stamp_duty(30000000)}円")
    print(f"仲介手数料: {calc.calculate_brokerage_fee(30000000)}")

    # 住所分割テスト
    print("\n=== 住所分割テスト ===")
    an = AddressNormalizer()
    result = an.split_address('東京都渋谷区道玄坂1-1')
    print(result)

    # 面積変換テスト
    print("\n=== 面積変換テスト ===")
    ac = AreaCalculator()
    print(f"150㎡ = {ac.convert_area(150, 'm2', 'tsubo'):.2f}坪")
    print(ac.format_area(45.45, 'tsubo'))
