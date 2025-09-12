import re

import re


def clean_text(text: str) -> str:
    # Giữ lại chữ cái, số, khoảng trắng, dấu chấm
    text = re.sub(r"[^a-zA-Z0-9àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễ"
                  r"ìíịỉĩòóọỏõôồốộổỗơờớợởỡ"
                  r"ùúụủũưừứựửữỳýỵỷỹđĐ\s.]", "", text)

    # Gom nhiều dấu chấm liên tiếp thành 1
    text = re.sub(r"\.{2,}", ".", text)

    # Rút gọn nhiều khoảng trắng thành 1 khoảng trắng
    text = re.sub(r"\s+", " ", text).strip()

    # Xóa khoảng trắng ngay sau dấu chấm
    text = re.sub(r"\.\s+", ".", text)

    return text


def convertTextToArrayTextLessThanXCharacter(x: str, number: int):
    texts = x.split(".")
    res = []
    cnt_char = 0
    value = ""
    for text in texts:
        cnt_char += len(text)
        value += text
        if cnt_char > number:
            res.append(value)
            cnt_char = 0
            value = ""
    if value:
        res.append(value)
    return res


s = '''
Lâm Tuyết khó khăn nói: "Tiểu thư từ nhỏ đã rất hiểu chuyện, cậu bị thương quá nặng, nếu không có viên Sinh Cơ Tạo Hóa Đan kia... chỉ có nó, mới cứu được mạng cậu."
Nhìn thấy vẻ khổ sở và bất lực sâu sắc giữa đôi lông mày của Lâm Tuyết, Diệp Thiên không hỏi thêm nữa. Bất luận thế nào, hắn tuyệt đối không để em gái mình vì hắn mà gả cho một tên chỉ biết ăn chơi trác táng, ức hiếp kẻ yếu, đó là hạnh phúc cả đời của em gái hắn. Bây giờ Diệp Thiên có thể làm là cố gắng hết tốc độ hồi phục vết thương, chỉ cần hồi phục vết thương, mọi vấn đề sẽ được giải quyết.
"Từ khi Hầu gia biến mất, phủ đệ Vô Địch Hầu chúng ta... ai." Lâm Tuyết thở dài.
Diệp Thiên lục lọi ký ức, phụ thân kiếp này của hắn được xưng là Vô Địch Hầu, tuy được gọi là hầu, nhưng thực lực và địa vị lại không hề kém Chiến Vương phủ chút nào, thậm chí còn vững chắc hơn một bậc. Nhưng mười bốn năm trước, không lâu sau khi Diệp Thiên ra đời, Vô Địch Hầu Diệp Kình Thương vì muốn hắn có thể nâng cao thiên phú, đã quyết đoán đến cấm địa Lôi Kiếp tìm kiếm Lôi Linh, nhưng từ đó đến nay, mười bốn năm đã trôi qua, không còn tin tức gì về ông nữa. Gần như tất cả mọi người đều cho rằng Vô Địch Hầu Diệp Kình Thương đã không còn, điều này dẫn đến việc gia đình Diệp Thiên hiện tại cuộc sống còn không bằng cả người hầu nhà người khác.
Ầm!
Ngay lúc này, cửa phòng bị người ta đạp mạnh, một đám người hung hãn xông vào. Trong đám người đó, kẻ cầm đầu là một trung niên tướng mạo dữ tợn, bàn tay hắn to dị thường, gần gấp đôi người thường, lờ mờ có thể thấy, dấu tay này khớp với vết tát trên mặt Lâm Tuyết.
"Vương Mãn, ngươi dám xông vào phủ đệ của ta, không sợ quốc chủ trách phạt sao?" Lâm Tuyết lập tức giận dữ quát lớn, rút trường kiếm trong tay, nghiêm nghị đối diện. Trên thân kiếm có khắc hai chữ "Vô Địch", là thanh kiếm mà Vô Địch Hầu trước khi đi đến cấm địa Lôi Kiếp, để đánh lạc hướng dư luận, cũng là để bảo vệ người nhà, đã giao cho Lâm Tuyết bí mật cất giữ. Mấy ngày nay phủ đệ không yên ổn, nàng mới lấy nó ra.
Vương Mãn cười khẩy, thản nhiên dẫn người bước vào, lạnh nhạt nói: "Xông vào thì không phải, bọn ta hôm nay đến là để đưa lễ vật, chứ không phải đến gây sự. Hơn nữa, các ngươi muốn báo lên, cũng phải có khả năng rời khỏi phủ đệ này đã."
"Ngươi, ngươi..." Lâm Tuyết tức giận đến mức không thốt nên lời.
Diệp Thiên nhìn thấy tất cả, trong lòng tràn ngập phẫn nộ, nhưng hắn lúc này vẫn không thể cử động, thương thế trong người quá nặng. Thiên phú của Diệp Thiên ở kiếp này quá kém cỏi, tu luyện mười sáu năm mới miễn cưỡng đạt tới Luân Hải cảnh tầng một, hơn nữa kinh mạch trong cơ thể tắc nghẽn, khó khăn trong việc tu hành. Hai kiếp trước Diệp Thiên đều là người đứng đầu kiếm đạo, cho dù hiện tại hắn chỉ có tu vi Luân Hải cảnh tầng một, kiếm pháp 《Vô Khuyết》ngộ ra khi chuyển thế ở kiếp thứ ba, đối mặt với người mạnh Hồn Linh cảnh vẫn có thể gắng sức, chỉ cần là tu sĩ dưới Hồn Linh cảnh, đều có thể dễ dàng đánh bại. Mà Vương Mãn dẫn đầu cũng chỉ có tu vi Luân Hải cảnh tầng bảy, mười mấy tên thuộc hạ của hắn còn yếu hơn, đều ở khoảng Luân Hải cảnh tầng bốn đến tầng năm. Đối mặt với kẻ địch như vậy, Diệp Thiên chỉ cần một kiếm là có thể giải quyết. Nhưng điều kiện tiên quyết là hắn phải hồi phục trước đã.
Lúc này Diệp Thiên đang vận chuyển 《Luân Hồi Tái Sinh Thuật》 để hồi phục tu vi, chỉ cần một khoảng thời gian ngắn là có thể khôi phục khả năng hành động. 《Luân Hồi Tái Sinh Thuật》 ở đại lục bao la này, có vô vàn truyền thuyết thần bí, ngay cả người tu đạo đỉnh cao cũng muốn có được, nhưng trên thế gian này chỉ có Diệp Thiên, người đã hai lần là người đứng đầu, có được nó. Bí thuật này là bí thuật chữa trị lợi hại nhất, cũng là phương pháp rèn luyện thân thể tối thượng, không gì sánh bằng. Giờ khắc này, hắn chỉ có thể nhẫn nhịn.
"Đưa lễ vật lên đây!" Vương Mãn khẽ quát.
'''
# text_new = clean_text(s)
# print(len(text_new))
# res = convertTextToArrayTextLessThan3000Character(text_new)
# print(len(res))
# print(res)
