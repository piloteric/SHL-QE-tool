import easyocr
import csv
import os

# 初始化 EasyOCR Reader，指定語言
reader = easyocr.Reader(['en'])

# 獲取腳本所在的目錄
script_directory = os.path.dirname(os.path.realpath(__file__))

# 設定圖片所在目錄為腳本所在的目錄
image_folder = script_directory

# 打開 CSV 文件並準備寫入
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # 寫入 CSV 文件標題
    csv_writer.writerow(['name', 'number', 'temp'])

    # 遍歷目錄中的所有圖片文件
    for image_filename in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_filename)

        # 檢查文件是否為圖片（可根據需要修改檢查條件）
        if image_filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            print(f"Processing image: {image_filename}")
            result = reader.readtext(image_path)

            # 用來儲存每行的文本
            row = [image_filename]

            # 處理結果並按需求填充
            for i, (bbox, text, prob) in enumerate(result):
                # 如果是偶數行，放在第一列
                if i % 2 == 0:
                    row.append(text)
                else:
                    # 如果是奇數行，放在第二列並寫入 CSV
                    row.append(text)
                    csv_writer.writerow(row)
                    row = [image_filename]  # 清空當前行，保證第一列是圖片名

            # 如果最後還有剩餘的文本在 "row" 中（只有一個元素的情況）
            if len(row) > 1:  # 如果最後一行的第二列為空，則跳過
                row.append('')  # 如果第二列沒有文本，填充空白
                csv_writer.writerow(row)

print('inference finished')
