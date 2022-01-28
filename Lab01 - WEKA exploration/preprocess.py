#-------------------------------------------Hướng dẫn sử dụng tham số dòng lệnh-------------------------------------------
# 1. python3 preprocess.py house-prices.csv --function=list-missing
# 2. python3 preprocess.py house-prices.csv --function=row-missing
# 3. python3 preprocess.py house-prices.csv --function=fill-missing-values --method=<mean, median> --out=result.csv
# 4. python3 preprocess.py house-prices.csv --function=drop-missing-row --out=result.csv <phần trăm>
# 5. python3 preprocess.py house-prices.csv --function=drop-missing-column --out=result.csv <phần trăm>
# 6. python3 preprocess.py house-prices.csv --function=drop-duplicate-values <-i, -a, -p <phần trăm>> --out=result.csv
# 7. python3 preprocess.py house-prices.csv --function=normalization --method=<min_max, z_score> -a --out=result.csv
#    python3 preprocess.py house-prices.csv --function=normalization --method=<min_max, z_score> --out=result.csv --attribute=<tên các thuộc tính>
# 8. python3 preprocess.py house-prices.csv --function=calculation --out=result.csv

#-------------------------------------------Luồng chạy chính-------------------------------------------
# Khai báo các thư viện cần thiết
import sys
import getopt
import pandas as pd

def get_missing_cols(df):
    missing_cols = []
    
    for col in df:
        for item in df[col]:
            if item != item: # if item is None
                missing_cols.append(col)
                break
    return missing_cols


def main():
    # Khai báo và tiền xử lý tham số dòng lệnh
    input_file = sys.argv[1]
    output_file = None
    df = pd.read_csv(input_file)
    option = 'default'
    numeric_cols = ['LotFrontage', 'LotArea', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'TotalBsmtSF',
                    '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'GarageArea', 'WoodDeckSF',
                    'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal', 'SalePrice']

    try:
        opts, args = getopt.getopt(sys.argv[2:], 'iap:', ['function=', 'attribute=', 'method=', 'out='])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--function':
            function = arg
        elif opt == '--method':
            method = arg
        elif opt == '-i':
            option = 'id'
        elif opt == '-a':
            option = 'all'
        elif opt == '-p':
            option = 'percent'
            percent = float(arg)
        elif opt == '--out':
            output_file = arg
        elif opt == '--attribute':
            option = 'custom'
            attributes = [arg]
        elif opt == '':
            print('yes')

    if function in ['drop-missing-row', 'drop-missing-column']:
        percent = float(args[0])
    if option == 'custom':
        attributes += args
        
    # 1. Liệt kê các cột bị thiếu dữ liệu
    if function == 'list-missing':
        missing_cols = get_missing_cols(df)
        print(missing_cols)

    # 2. Đếm số dòng bị thiếu dữ liệu
    elif function == 'row-missing':
        missing_rows = []
        for i in range(len(df['Id'])):
            row = [df[col][i] for col in df] # Chuyển 1 dòng thành kiểu list
            
            # Nếu tồn tại dòng có phần tử = NaN thì dòng đó bị thiếu dữ liệu
            if len([r for r in row if r != r]) != 0:
                missing_rows.append(row)

        # In ra màn hình số dòng bị thiếu dữ liệu
        print(len(missing_rows))

    # 3. Điền giá trị bị thiếu bằng phương pháp mean, median (cho thuộc tính numeric) và mode (cho thuộc tính categorical)
    # Lưu ý: Khi tính mean, median hay mode bỏ qua giá trị bị thiếu
    elif function == 'fill-missing-values':
        # Liệt kê các cột bị thiếu dữ liệu
        missing_cols = get_missing_cols(df)

        # Điền khuyết giá trị bị thiếu chon từng cột trong missing_cols
        for col in missing_cols:
            # Liệt kê các phần tử != NaN trong từng cột
            full_item = [item for item in df[col] if item == item]

            # Trường hợp 1: Cột dữ liệu là thuộc tính categorical -> Tính mode
            if len(full_item) != 0 and col not in numeric_cols:
                # Tạo bảng tần số xuất hiện của mỗi phần tử category với trường 'name' (tên phần tử) và 'total' (số lần xuất hiện) 
                dt_item = []
                for item in list(set(full_item)):
                    dt_item.append({'name': item, 'total': len([i for i in full_item if i == item])})
                
                # Tìm phần tử có số lần xuất hiện nhiều nhất
                max_val = max([item['total'] for item in dt_item])
                # Tìm mode
                missing_val = [item['name'] for item in dt_item if item['total'] == max_val][0]
                
                # Gán phần tử là giá trị thiếu = missing_val
                df[col] = [missing_val if item != item else item for item in df[col]]

            # Trường hợp 2: Cột dữ liệu là thuộc tính numeric -> tính mean hoặc med
            elif len(full_item) != 0 and col in numeric_cols:
                # Tìm mean
                if method == 'mean':
                    missing_val = round(sum(full_item) / len(full_item), 3)
                # Tìm median
                else:
                    if len(full_item) % 2 != 0:
                        missing_val = full_item[len(full_item) // 2] # = med
                    else:zz
                        missing_val = round((full_item[len(full_item) // 2] + full_item[len(full_item) // 2 - 1])/2, 3)
                # Gán phần tử là giá trị thiếu = missing_val
                df[col] = [missing_val if item != item else item for item in df[col]]

        # Viết dữ liệu vào file csv
        df.to_csv(output_file, sep = ',', encoding = 'UTF-8', index = False)
        # In ra màn hình các bảng dữ liệu sau khi thay đổi
        print(df)
        
    # 4. Xóa các dòng bị thiếu dữ liệu với ngưỡng tỉ lệ thiếu cho trước
    elif function == 'drop-missing-row':
        new_df = {col: [] for col in df}

        for i in range(len(df['Id'])):
            row = [df[col][i] for col in df]
            
            # đếm có bao nhiêu thuộc tính thiếu NaN (r != r) và dò số thuộc tính thiếu với ngưỡng percent đầu vào, nếu thỏa bé hơn thì dòng đó dươc chấp nhận và add vào new_df
            if (len([r for r in row if r != r]) / len(row)) < (percent / 100):
                for j, col in zip(range(len(row)), df):
                    new_df[col].append(row[j])

        # Viết dữ liệu vào file csv
        df = pd.DataFrame(new_df)
        df.to_csv(output_file, sep = ',', encoding = 'UTF-8', index = False)
        # In ra màn hình các bảng dữ liệu sau khi thay đổi
        print(df)

    # 5. Xóa các cột bị thiếu dữ liệu với ngưỡng tỉ lệ thiếu cho trước
    elif function == 'drop-missing-column':
        new_df = {}

        for col in df:
            # với mỗi cột, nếu (% giá trị NaN) < (ngưỡng đầu vào) -> chấp nhận cột đó; ngược lại thì không
            if (len([item for item in df[col] if item != item]) / len(df[col])) < (percent / 100):
                new_df[col] = df[col]

        # Viết dữ liệu vào file csv
        df = pd.DataFrame(new_df)
        df.to_csv(output_file, sep = ',', encoding = 'UTF-8', index = False)
        # In ra màn hình các bảng dữ liệu sau khi thay đổi
        print(df)

    # 6. Xóa các mẫu bị trùng lặp. Có 3 cách xử lý cho chức năng này:
    # - Cách 1: Loại bỏ các mẫu có trùng Id với nhau
    # - Cách 2: Loại bỏ các mẫu có trùng lặp tất cả các thuộc tính
    # - Cách 3: Loại bỏ các mẫu có trùng hơn (percent)% thuộc tính 
    elif function == 'drop-duplicate-values':
        # Khởi tạo dict mới new_df
        new_df = {col:[] for col in df}

        # Đọc toàn bộ dòng vào mảng all_rows
        all_rows = []
        for i in range(len(df['Id'])):
            all_rows.append([df[col][i] for col in df])

        # Loại bỏ các dòng có trùng lặp Id với nhau
        if option == 'id':
            for row in all_rows:
                # Duyệt từng dòng trong df để xem có Id nào tồn tại trong new_df
                # Nếu không có thì gán dòng đó vào dict new_df
                if row[0] not in new_df['Id']:
                    for j, col in zip(range(len(row)), df):
                        new_df[col].append(row[j])

        # Loại bỏ các dòng có trùng lặp tất cả các thuộc tính với nhau
        elif option == 'all':
            for row in all_rows:
                all_new_rows = []
                # Duyệt từng dòng trong all_rows để xem có dòng nào tồn tại trong all_new_rows. Nếu không tồn tại thì gán dòng đó vào dict new_df
                for i in range(len(new_df['Id'])):
                    all_new_rows.append([new_df[col][i] if new_df[col][i] == new_df[col][i] else 'None' for col in new_df])
                
                changed_row = [item if item == item else 'None' for item in row]
                if changed_row not in all_new_rows:
                    for j, col in zip(range(len(row)), new_df):
                        new_df[col].append(row[j])

        # Loại bỏ các dòng có trùng lặp hơn ngưỡng tỉ lệ cho trước
        elif option == 'percent':
            for row in all_rows:
                # Chuyển dict new_df thành dạng list all_new_rows
                all_new_rows = []
                for i in range(len(new_df['Id'])):
                    all_new_rows.append([new_df[col][i] if new_df[col][i] == new_df[col][i] else 'None' for col in new_df])
                # Duyệt từng dòng trong all_rows để tỉnh tỉ lệ phần trăm giống nhau
                changed_row = [item if item == item else 'None' for item in row]
                flag = False
                for new_row in all_new_rows:
                    # Các thuộc tính có trùng nhau của changed_row và new_row
                    duplicated_attr = [new_row[i] for i in range(len(new_row)) if changed_row[i] == new_row[i]]
                    # Tính tỉ lệ phần trăm trùng nhau
                    if len(duplicated_attr) / len(changed_row) * 100 >= percent:
                        flag = True
                        break
                # Nếu phần trăm tỉ lệ trùng >= percent thì gán dòng đó vào dict new_df
                if flag == False or len(all_new_rows) == 0:
                    for j, col in zip(range(len(row)), new_df):
                        new_df[col].append(row[j])

        # Viết dữ liệu vào file csv 
        df = pd.DataFrame(new_df)
        df.to_csv(output_file, sep = ',', encoding = 'UTF-8', index = False)
        # In ra màn hình các bảng dữ liệu sau khi thay đổi
        print(df)

    # 7. Chuẩn hóa một thuộc tính numeric bằng phương pháp min-max và z-score. Có 2 cách xử lý cho chức năng này:
    # Cách 1: Chuẩn hóa cho 1 vài (--attribute=<tên các thuộc tính>) thuộc tính numeric được nhập từ bàn phím
    # Cách 2: Chuẩn hóa cho tất cả (-a) các thuộc tính numeric
    elif function == 'normalization':
        true_nume_cols = []
        
        # Trường hợp chuẩn hóa cho tất cả các thuộc tính numeric
        if option == 'all':
            true_nume_cols = numeric_cols
        # chỉ chuẩn hóa đối với thuộc tính numeric trong input người dùng, cột không phải numeric thì báo console và không chuẩn hóa
        elif option == 'custom': 
            true_nume_cols = [col for col in attributes if col in numeric_cols]
            false_nume_cols = set(attributes) - set(numeric_cols)
            
            if len(false_nume_cols) != 0:
                print('Cannot normalize these attributes: ', ', '.join(false_nume_cols))
            # nếu tát cả thuộc tính nhập vào đều không phải thuộc tính numeric thì không thực hiện chuẩn hóa      
            if not true_nume_cols:
                return -1
                    
        # Xét các cột dữ liệu là thuộc tính numeric
        for col in true_nume_cols:
            # Liệt kê các phần tử != NaN trong từng cột
            full_item = [item for item in df[col] if item == item]

            if len(full_item) != 0 and col in true_nume_cols:
                if method == 'min_max':
                    # Tính min, max
                    min_val = min(full_item)
                    max_val = max(full_item)
                    
                    # nếu min_val = max_val thì thuộc tính đó không có ý nghĩa vì tất cả giá trị tại thuộc tính đó đều như nhau
                    if min_val != max_val:
                        df[col] = [round((item - min_val)/(max_val - min_val), 3) if item == item else item for item in df[col]] 
                elif method == 'z_score':
                    # Tính mean
                    mean_val = sum(full_item) / len(full_item)
                    
                    # Tính std
                    std_val = 0
                    for item in full_item:
                        std_val += (item - mean_val)**2
                    std_val = (std_val / len(full_item))**(0.5)
                    
                    # nếu std = 0 thì không có ý nghĩa, các giá trị trong thuộc tính đó đều bằng nhau & bằng 1 hằng số
                    if std_val:
                        df[col] = [round((item - mean_val)/(std_val), 3) if item == item else item for item in df[col]]  
            
        # Viết dữ liệu vào file csv
        df.to_csv(output_file, sep = ',', encoding = 'UTF-8', index = False)
        # In ra màn hình các bảng dữ liệu sau khi thay đổi
        print(df)

    # 8. Tính giá trị biểu thức thuộc tính
    elif function == 'calculation':
        # số năm mà 1 căn nhà không có người thuê
        df['YearAvailable'] = df['YrSold'] - df['YearBuilt']
        # tổng diện tích mái vòm 
        df['TotalPorchArea'] = df['OpenPorchSF'] + df['EnclosedPorch'] + df['3SsnPorch'] + df['ScreenPorch']

        # Viết dữ liệu vào file csv
        df.to_csv(output_file, sep = ',', encoding = 'UTF-8', index = False)
        # In ra màn hình các bảng dữ liệu sau khi thay đổi
        print(df)        

if __name__ == '__main__':
    main()