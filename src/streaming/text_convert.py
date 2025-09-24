
import re


# def clean_text(text: str) -> str | None:
#     if text is None:
#         return None
#
#         # 0. Chuẩn hóa: thay "…" thành "."
#     text = text.replace("…", ".")
#
#     # 1. Giữ lại chữ cái, số, khoảng trắng, dấu chấm, dấu phẩy
#     result = re.sub(r"[^\w\s.,]", "", text, flags=re.UNICODE)
#
#     # 2. Gom nhiều dấu chấm liên tiếp thành 1 dấu
#     result = re.sub(r"\.+", ".", result)
#
#     # 3. Xóa khoảng trắng thừa 2 bên
#     result = result.strip()
#
#     # 4. Bỏ khoảng trắng ngay sau dấu chấm
#     result = re.sub(r"\.\s*", ".", result)
#
#     # 5. Bỏ khoảng trắng ngay sau dấu phẩy
#     result = re.sub(r",\s*", ",", result)
#
#     # 6. Viết hoa chữ cái đầu mỗi câu sau dấu .
#     def capitalize_after_dot(match):
#         return match.group(1) + match.group(2).upper()
#
#     result = re.sub(r"(^|\.)(\w)", capitalize_after_dot, result)
#
#     return result


import re


def clean_text(text: str) -> str | None:
    if text is None:
        return None

    # 0. Chuẩn hóa ký tự đặc biệt
    text = text.strip()
    text = text.replace("…", ".")

    # 0.1. Thay xuống dòng thành dấu chấm
    text = re.sub(r"[\r\n]+", ".", text)

    # 1. Giữ lại chữ cái, số, khoảng trắng, dấu chấm, dấu phẩy
    result = re.sub(r"[^\w\s.,]", "", text, flags=re.UNICODE)

    # 2. Gom nhiều dấu chấm liên tiếp thành 1 dấu
    result = re.sub(r"\.+", ".", result)

    # 3. Xóa khoảng trắng thừa 2 bên
    result = result.strip()

    # 4. Bỏ khoảng trắng ngay sau dấu chấm
    result = re.sub(r"\.\s*", ".", result)

    # 5. Bỏ khoảng trắng ngay sau dấu phẩy
    result = re.sub(r",\s*", ",", result)

    # 6. Viết hoa chữ cái đầu mỗi câu sau dấu .
    def capitalize_after_dot(match):
        return match.group(1) + match.group(2).upper()

    result = re.sub(r"(^|\.)(\w)", capitalize_after_dot, result)

    # 7. Viết hoa chữ cái đầu tiên toàn bộ chuỗi
    if result:
        result = result[0].upper() + result[1:]

    return result


s = '''
Thành phố Lâm nằm bên bờ sông Bích Ba. Mỗi khi mùa xuân về, cả thành phố phảng phất được bao trùm bởi sương mù ẩm ướt và mát lạnh.

Một ngày sắc trời u ám bình thường, cục cảnh sát thành phố có một sự xao động bất thường.

Bởi vì đại đội cảnh sát hình sự xuất hiện hai nữ cảnh sát thực tập trẻ tuổi.

Đây vốn không phải chuyện to tát. Nhưng hai cô gái trẻ mới ngồi trong văn phòng một lúc đã thu hút sự chú ý của không ít cảnh sát, có người thậm chí thò đầu vào cửa quan sát hai cô gái.

Bởi vì trông bọn họ rất đặc biệt.

Anh chàng cảnh sát trẻ tuổi Triệu Hàn là người liên lạc thực tập của hai cô gái. Lúc này, anh cũng như các đồng nghiệp khác, ngẩn người nhìn hai cô gái trẻ trước mặt.

Một cô rất xinh đẹp, còn một cô...trông hơi kỳ quái.

Cô gái ngồi bên tay trái tên Diêu Mông, là nghiên cứu sinh tâm lý tội phạm đại học Công an. Cô có đôi mắt to và mái tóc dài, tuy chỉ mặc quần jeans và áo sơ mi trắng đơn giản, nhưng vẫn giống người mẫu bước ra từ tạp chí tuổi trẻ. Sơ yếu lý lịch của cô tương đối hoành tráng: Học bổng của nhà trường, cán bộ xuất sắc, người chủ trì chương trình phát thanh của trường, Top 10 tuyển thủ xuất sắc trong cuộc thi hùng biện...

Triệu Hàn có dự cảm, Diêu Mông sẽ trở thành hoa khôi mới của ngành cảnh sát thành phố Lâm.

Cô gái còn lại tên là Hứa Hủ...

Trên sơ yếu lý lịch, thành thích của Hứa Hủ rất xuất sắc, năm nào cũng đứng đầu toàn trường đại học.

Nhưng Triệu Hàn nghi ngờ, không biết cô làm thế nào để thi vào trường công an. Bởi vì cô có vẻ không cao tới một mét sáu. Thân hình cô vừa gầy vừa nhỏ bé, dù ngồi nghiêm chỉnh trên ghế cũng giống thiếu nữ vị thành niên. Làn da cô trắng đến mức không một chút sắc hồng, ngũ quan thuộc loại bình thường. Nhìn lướt qua, trông cô giống...đúng rồi, giống nhân vật ma cà rồng trong phim Mỹ. Nhưng cô lại mặc chiếc áo khoác dài màu đen nghiêm chỉnh, áo khoác dài đến tận mắt cá chân, không hợp với bộ dạng non nớt của cô, khiến cô có vẻ kỳ quái và buồn cười.

Tên của cô, Hứa Hủ, đọc là Xuxu?

Suỵt Suỵt? (phiên âm của từ "suỵt" cũng là "xu", giống tên của Hứa Hủ)

Triệu Hàn hơi buồn cười, nhưng vốn là một chàng trai trẻ hiền hậu và lịch sự, nên anh vẫn giữ vẻ mặt ôn hòa, thôi không quan sát Hứa Hủ.

Anh vừa định mở miệng, đúng lúc Hứa Hủ ngẩng đầu nhìn anh.

Ánh mắt của cô khiến Triệu Hàn hơi ngây người.

Mấy phút trước đó đều là Diêu Mông trò chuyện với anh, Hứa Hủ chỉ trầm mặc lắng nghe, thậm chí dường như chưa từng nhìn thẳng anh một lần.

Bây giờ Triệu Hàn mới phát giác, đồng tử của cô đặc biệt đen, đen đến mức khó diễn ra. Ánh mắt cô vô cùng bình thản và đúng mực.

Anh đột nhiên có cảm giác, cô đã nhìn thấu suy nghĩ của anh, cô biết anh nghĩ gì về cô.

Nhưng chỉ trong chớp mắt, Hứa Hủ lại cúi đầu, khôi phục bộ dạng trắng bệch uể oải đó.

Triệu Hàn ho khan một tiếng: "Mấy ngày này Quý đội phó nghỉ phép không đi làm. Khi nào anh ấy trở về, anh ấy sẽ quyết định thầy giáo hướng dẫn thực tập của hai em."

Mắt Diêu Mông đột nhiên sáng ngời: "Có phải là tiền bối Quý Bạch, người có tỷ lệ phá án cao nhất ở khu vực Tây Nam không ạ?"

Triệu Hàn mỉm cười gật đầu.

"Liệu anh ấy có hướng dẫn bọn em không?" Hứa Hủ bất chợt nói xen ngang, thanh âm của cô mềm mại yếu ớt.

Triệu Hàn trả lời: "Phải đợi Quý đội về mới quyết định."

Quý Bạch không xa lạ với giới nữ cảnh sát trẻ tuổi trẻ. Mọi người đều nói, anh có bề ngoài nho nhã nhưng tiếp xúc lâu ngày mới biết, anh đẹp trai bao nhiêu thì bụng dạ cứng rắn bấy nhiêu, bất kể là đối với tội phạm hay đối với những cô gái có cảm tình với anh.

Vì vậy, mặc dù cục trưởng từng đích thân dặn dò, để đội phó đại đội cảnh sát hình sự Quý Bạch và một cảnh sát có kinh nghiệm dẫn dắt hai sinh viên xuất sắc này. Nhưng Triệu Hàn hiểu rõ tính cách của Quý Bạch, anh làm sao đủ lòng nhẫn nại hướng dẫn sinh viên thực tập? Còn là nữ sinh yếu ớt?

"Anh là người liên lạc thực tập của các em. Gặp bất cứ chuyện gì các em đều có thể tìm anh." Triệu Hàn nói: "Đây là tài liệu "Thực tập cần biết", các em hãy xem đi."

Hai cô gái nhận tập tài liệu, xem rất chăm chú. Một lúc sau, thấy hai cô không lên tiếng thắc mắc, Triệu Hàn mới cất giọng hiếu kỳ: "Cho anh hỏi một câu, các em học ngành này, vậy các em cảm thấy phân tích tâm lý có tác dụng đối với việc phá án hay không?"

Triệu Hàn vừa dứt lời, Diêu Mông trả lời ngay: "Em thấy rất hữu dụng, nhưng chúng em mới chỉ nắm một số lý luận, thiếu kinh nghiệm vận dụng thực tế. Vì vậy từ nay về sau, bọn em chắc sẽ thường xuyên cần thỉnh giáo anh Triệu. Đến lúc đó mong anh đừng chê phiền phức."

Triệu Hàn mỉm cười: "Em đừng khách sáo, chúng ta học tập lẫn nhau."

Anh đưa mắt qua Hứa Hủ, cô gật đầu nhè nhẹ: "Em cũng nghĩ vậy." Sau đó cô liền ngậm miệng, dường như không muốn nói một câu thừa thãi.

Triệu Hàn nghĩ thầm, cô gái này đúng là không biết giao tiếp, sau này trong công việc chỉ e sẽ vấp phải trắc trở.

Diêu Mông ở bên cạnh vẫn mỉm cười ngọt ngào, tựa hồ đã quen với thái độ lạnh nhạt của Hứa Hủ. Nhưng ánh mắt của cô nhìn Triệu Hàn, toát ra vẻ áy náy bất lực.

Có điều Triệu Hàn không để tâm, anh vừa cười vừa nói đùa: "Hai em thử phân tích con người anh, xem ai nói chuẩn hơn?"

Người bình thường luôn coi phân tích tâm lý là một loại mơ hồ bí ẩn như đoán số mệnh, anh chàng cảnh sát trẻ tuổi lắm lời này cũng không ngoại lệ.

Diêu Mông chớp mắt: "Anh Triệu, đây là đề thi sao?

"Cứ coi như đề thi đầu tiên của các em trong thời gian thực tập đi."

Những người khác thuộc đội cảnh sát hình sự đều đi họp hoặc ra ngoài, trong phòng chỉ còn lại ba bọn họ. Ánh nắng buổi chiều chiếu vào cửa sổ, khiến văn phòng vừa sáng sủa vừa trống trải.

Triệu Hàn bị hai cô gái trẻ nhìn dò xét từ trên xuống dưới, anh bất giác hơi hồi hộp.

Ánh mắt thanh lạnh của Hứa Hủ dừng lại trên mặt Triệu Hàn. Triệu Hàn tưởng cô sẽ mở miệng, ai ngờ cô vẫn trầm lặng như cũ, ngón tay cô đặt trên đầu gối, phảng phất gõ nhịp nhàng theo quán tính.

Thân hình nhỏ bé yếu ớt nhưng cô lại có động tác của một người đàn ông. Ngón tay cô vừa trắng vừa thanh mảnh, tựa hồ có thể gãy bất cứ lúc nào, khiến Triệu Hàn bỗng có cảm giác khó chịu không diễn tả thành lời.

Một lúc sau, ánh mắt của Diêu Mông cũng quay về mặt Triệu Hàn, bộ dạng của cô nóng lòng muốn thử sức.
'''
print(clean_text(s))





