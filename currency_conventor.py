import requests
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# 貨幣轉換函數
def crnc_cvt(api_key, from_crnc, to_crnc, amount):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_crnc}/{to_crnc}/{amount}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and data.get('result') == 'success':
            cvt_amount = data['conversion_result']
            conversion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = f"{amount} {from_crnc} 為 {cvt_amount} {to_crnc}。\n轉換時間: {conversion_time}"
            return result
        else:
            return f"資料擷取失敗: {data.get('error-type', '未知錯誤')}"
    except requests.exceptions.RequestException as e:
        return f"連接錯誤: {e}"

# 獲取所有支持的貨幣代碼
def get_supported_currencies(api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/codes"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and data.get('result') == 'success':
            # 提取貨幣代碼並返回
            return [f"{code} ({name})" for code, name in data['supported_codes']]
        else:
            messagebox.showerror("錯誤", "無法獲取貨幣代碼")
            return []
    except requests.exceptions.RequestException as e:
        messagebox.showerror("錯誤", f"連接錯誤: {e}")
        return []

# GUI 主界面
def gui_interface():
    def convert_currency():
        from_crnc = from_currency_var.get().split()[0]  # 提取貨幣代碼
        to_crnc = to_currency_var.get().split()[0]
        try:
            amount = float(amount_entry.get())
            result = crnc_cvt(api_key, from_crnc, to_crnc, amount)
            result_label.config(text=result)
        except ValueError:
            messagebox.showerror("輸入錯誤", "請輸入有效的金額")
    
    # 創建主視窗
    root = tk.Tk()
    root.title("貨幣轉換工具")
    
    # 當前貨幣選單
    from_currency_label = tk.Label(root, text="當前貨幣:")
    from_currency_label.grid(row=0, column=0, padx=10, pady=5)
    
    from_currency_var = tk.StringVar(root)
    from_currency_combobox = ttk.Combobox(root, textvariable=from_currency_var, width=30)
    from_currency_combobox.grid(row=0, column=1, padx=10, pady=5)
    
    # 目標貨幣選單
    to_currency_label = tk.Label(root, text="目標貨幣:")
    to_currency_label.grid(row=1, column=0, padx=10, pady=5)
    
    to_currency_var = tk.StringVar(root)
    to_currency_combobox = ttk.Combobox(root, textvariable=to_currency_var, width=30)
    to_currency_combobox.grid(row=1, column=1, padx=10, pady=5)
    
    # 金額輸入框
    amount_label = tk.Label(root, text="轉換數量:")
    amount_label.grid(row=2, column=0, padx=10, pady=5)
    
    amount_entry = tk.Entry(root)
    amount_entry.grid(row=2, column=1, padx=10, pady=5)
    
    # 轉換按鈕
    convert_button = tk.Button(root, text="開始轉換", command=convert_currency)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    # 顯示結果的標籤
    result_label = tk.Label(root, text="", wraplength=300, justify="left")
    result_label.grid(row=4, column=0, columnspan=2, pady=10)
    
    # 動態更新選單中的貨幣選項
    currencies = get_supported_currencies(api_key)
    
    from_currency_combobox['values'] = currencies
    to_currency_combobox['values'] = currencies
    
    # 設置可滾動選單和輸入查詢
    from_currency_combobox.config(state='normal')
    to_currency_combobox.config(state='normal')
    
    # 運行主循環
    root.mainloop()

# 主函數
def main():
    print("選擇轉換介面:")
    print("1. 命令行介面")
    print("2. GUI 介面")
    choice = input("請選擇 (1/2): ")
    
    if choice == '1':
        command_line_interface()
    elif choice == '2':
        gui_interface()
    else:
        print("無效的選擇。")

# 命令行介面函數
def command_line_interface():
    while True:
        from_crnc = input("請輸入當前貨幣:").upper()
        to_crnc = input("請輸入要轉換的貨幣:").upper()
        amount = float(input("請輸入貨幣轉換數量:"))
        
        result = crnc_cvt(api_key, from_crnc, to_crnc, amount)
        print(result)
        
        continue_query = input("要繼續查詢嗎？(Y/N): ").strip().lower()
        if continue_query != 'y':
            print("結束查詢。")
            break

# 個人的 API key
api_key = "d5ed7f22fb2a1661b5103ba1"

if __name__ == "__main__":
    main()
