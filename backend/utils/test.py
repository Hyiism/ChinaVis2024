from datetime import datetime

datetime_str2 = datetime.strftime(datetime.fromtimestamp(1704209872), '%Y-%m-%d %H:%M:%S')
print(datetime_str2)