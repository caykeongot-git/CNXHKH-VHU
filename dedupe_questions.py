# -*- coding: utf-8 -*-
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Dictionary of replacement questions mapped to question ID
REPLACEMENTS = {
    # --- CHAPTER 2 REPLACEMENTS (2 questions: 53, 84) ---
    53: {
        "question": "Tính chất cách mạng triệt để của sứ mệnh lịch sử giai cấp công nhân thể hiện ở chỗ nào?",
        "options": {
            "A": "Giải phóng giai cấp công nhân đồng thời giải phóng toàn thể nhân dân lao động khỏi mọi sự áp bức, bóc lột.",
            "B": "Chỉ đấu tranh cải thiện điều kiện sống và tiền lương cho người lao động.",
            "C": "Thỏa hiệp với giai cấp tư sản để duy trì trật tự xã hội cũ.",
            "D": "Duy trì chế độ tư hữu tư bản chủ nghĩa dưới hình thức công ty cổ phần."
        },
        "correct_answer": "A",
        "explanation": "Giai cấp công nhân giải phóng bản thân mình đồng thời giải phóng toàn bộ xã hội khỏi mọi gông cồng áp bức."
    },
    84: {
        "question": "Mục tiêu cuối cùng trong sứ mệnh lịch sử của giai cấp công nhân là gì?",
        "options": {
            "A": "Xây dựng thành công xã hội cộng sản chủ nghĩa không còn giai cấp và áp bức.",
            "B": "Trở thành giai cấp thống trị duy nhất cai trị vĩnh viễn xã hội.",
            "C": "Giành thắng lợi trong các cuộc bãi công tự phát.",
            "D": "Tạo ra sự bình đẳng về tài sản tư hữu giữa các tầng lớp."
        },
        "correct_answer": "A",
        "explanation": "Mục tiêu cao nhất của sứ mệnh lịch sử GCCN là giải phóng con người, xây dựng hình thái kinh tế - xã hội cộng sản chủ nghĩa."
    },

    # --- CHAPTER 3 REPLACEMENTS (13 questions: 102, 103, 107, 112, 114, 118, 119, 122, 124, 125, 126, 127, 129) ---
    102: {
        "question": "Theo V.I. Lênin, đặc trưng kinh tế nổi bật nhất của thời kỳ quá độ lên chủ nghĩa xã hội là gì?",
        "options": {
            "A": "Sự tồn tại nền kinh tế nhiều thành phần với các hình thức sở hữu khác nhau.",
            "B": "Nền kinh tế thuần nhất chỉ có một thành phần kinh tế nhà nước.",
            "C": "Nền kinh tế tự cấp tự túc phi hàng hóa.",
            "D": "Sự thống trị tuyệt đối của thành phần kinh tế tư nhân tư bản."
        },
        "correct_answer": "A",
        "explanation": "Trong thời kỳ quá độ, nền kinh tế tất yếu tồn tại nhiều thành phần do chưa xóa bỏ hoàn toàn tàn dư cũ."
    },
    103: {
        "question": "Nội dung cơ bản nhất của thời kỳ quá độ lên chủ nghĩa xã hội trên lĩnh vực tư tưởng - văn hóa là gì?",
        "options": {
            "A": "Xây dựng nền văn hóa mới XHCN và hệ tư tưởng Mác - Lênin giữ vai trò chủ đạo.",
            "B": "Duy trì nguyên vẹn các hủ tục và tập quán cũ của xã hội tư bản.",
            "C": "Nhập khẩu nguyên bản tư tưởng và văn hóa phương Tây.",
            "D": "Xóa bỏ hoàn toàn văn hóa truyền thống dân tộc."
        },
        "correct_answer": "A",
        "explanation": "Tư tưởng Mác - Lênin giữ vai trò chủ đạo trong đời sống tinh thần của xã hội thời kỳ quá độ."
    },
    107: {
        "question": "Hình thái kinh tế - xã hội cộng sản chủ nghĩa bao gồm những giai đoạn phát triển nào?",
        "options": {
            "A": "Giai đoạn thấp (chủ nghĩa xã hội) và giai đoạn cao (chủ nghĩa cộng sản).",
            "B": "Giai đoạn phong kiến và giai đoạn tư bản chủ nghĩa.",
            "C": "Giai đoạn quá độ và giai đoạn tư bản nhà nước.",
            "D": "Giai đoạn sản xuất nhỏ và giai đoạn đại công nghiệp."
        },
        "correct_answer": "A",
        "explanation": "Hình thái kinh tế - xã hội CSCN trải qua giai đoạn thấp (XHCN) và giai đoạn cao (CSCN)."
    },
    112: {
        "question": "Tại sao sự xuất hiện của chế độ công hữu về tư liệu sản xuất lại là yếu tố quyết định bản chất của chủ nghĩa xã hội?",
        "options": {
            "A": "Vì nó xóa bỏ cơ sở kinh tế của chế độ người bóc lột người.",
            "B": "Vì nó giúp tăng nhanh tư bản tư nhân cho giai cấp tư sản.",
            "C": "Vì nó biến mọi của cải thành sở hữu cá nhân.",
            "D": "Vì nó loại bỏ hoàn toàn vai trò của lao động sáng tạo."
        },
        "correct_answer": "A",
        "explanation": "Chế độ công hữu về TLSX loại bỏ căn nguyên bóc lột và bất bình đẳng kinh tế."
    },
    114: {
        "question": "Con đường quá độ lên chủ nghĩa xã hội bỏ qua chế độ tư bản chủ nghĩa ở Việt Nam được hiểu là:",
        "options": {
            "A": "Bỏ qua việc xác lập vị trí thống trị của quan hệ sản xuất và kiến trúc thượng tầng TBCN.",
            "B": "Bỏ qua toàn bộ lực lượng sản xuất và kỹ thuật công nghệ tiên tiến của TBCN.",
            "C": "Bỏ qua nền kinh tế thị trường và quan hệ giao thương quốc tế.",
            "D": "Bỏ qua quá trình công nghiệp hóa, hiện đại hóa đất nước."
        },
        "correct_answer": "A",
        "explanation": "Bỏ qua chế độ TBCN là bỏ qua vị trí thống trị của QHSX và KTTT tư bản chủ nghĩa."
    },
    118: {
        "question": "Nhiệm vụ trọng tâm xuyên suốt của thời kỳ quá độ lên chủ nghĩa xã hội ở Việt Nam là gì?",
        "options": {
            "A": "Đẩy mạnh công nghiệp hóa, hiện đại hóa đất nước gắn với phát triển kinh tế tri thức.",
            "B": "Duy trì sản xuất nông nghiệp lạc hậu tự cung tự cấp.",
            "C": "Hạn chế mở rộng hợp tác kinh tế quốc tế.",
            "D": "Tập trung phát triển ngành kinh tế cá thể tiểu nông."
        },
        "correct_answer": "A",
        "explanation": "Công nghiệp hóa, hiện đại hóa là nhiệm vụ trung tâm để xây dựng cơ sở vật chất kỹ thuật cho CNXH."
    },
    119: {
        "question": "Trong thời kỳ quá độ lên chủ nghĩa xã hội, quy luật phân phối chủ đạo nào được áp dụng?",
        "options": {
            "A": "Phân phối theo lao động.",
            "B": "Phân phối bình quân theo đầu người.",
            "C": "Phân phối theo mức độ sở hữu tư bản.",
            "D": "Phân phối theo nhu cầu cá nhân tự do."
        },
        "correct_answer": "A",
        "explanation": "Trong giai đoạn thấp của xã hội CSCN, phân phối theo lao động là nguyên tắc phân phối chủ đạo."
    },
    122: {
        "question": "Bản chất chính trị của thời kỳ quá độ lên chủ nghĩa xã hội được thể hiện thông qua việc:",
        "options": {
            "A": "Thiết lập chuyên chính vô sản và phát huy nền dân chủ xã hội chủ nghĩa.",
            "B": "Duy trì bộ máy nhà nước quân chủ chuyên chế.",
            "C": "Trao toàn bộ quyền lực chính trị cho giai cấp tư sản.",
            "D": "Xóa bỏ hoàn toàn pháp luật và bộ máy nhà nước."
        },
        "correct_answer": "A",
        "explanation": "Thực chất chính trị của thời kỳ quá độ là thiết lập nhà nước chuyên chính vô sản / nhà nước XHCN."
    },
    124: {
        "question": "Nguyên nhân kinh tế sâu xa dẫn đến sự ra đời của chủ nghĩa xã hội là gì?",
        "options": {
            "A": "Mâu thuẫn giữa lực lượng sản xuất mang tính xã hội hóa cao với quan hệ sản xuất tư nhân TBCN.",
            "B": "Sự thiếu hụt nguyên liệu sản xuất trên phạm vi toàn cầu.",
            "C": "Sự xuất hiện của công nghệ số và trí tuệ nhân tạo.",
            "D": "Sự gia tăng cạnh tranh giữa các tập đoàn đa quốc gia."
        },
        "correct_answer": "A",
        "explanation": "Mâu thuẫn giữa LLSX mang tính xã hội hóa và QHSX tư hữu TBCN đòi hỏi sự thay thế bằng QHSX công hữu XHCN."
    },
    125: {
        "question": "Cơ sở vật chất - kỹ thuật của chủ nghĩa xã hội được tạo ra từ nền sản xuất nào?",
        "options": {
            "A": "Nền đại công nghiệp hiện đại.",
            "B": "Nền kinh tế nông nghiệp tiểu nông.",
            "C": "Sản xuất thủ công truyền thống.",
            "D": "Kinh tế thương nghiệp giản đơn."
        },
        "correct_answer": "A",
        "explanation": "Chủ nghĩa xã hội phải dựa trên cơ sở vật chất kỹ thuật là nền đại công nghiệp hiện đại."
    },
    126: {
        "question": "Sự khác biệt căn bản giữa quá độ trực tiếp và quá độ gián tiếp lên chủ nghĩa xã hội là gì?",
        "options": {
            "A": "Quá độ gián tiếp diễn ra ở các nước chưa trải qua chủ nghĩa tư bản phát triển.",
            "B": "Quá độ trực tiếp không cần sự lãnh đạo của Đảng Cộng sản.",
            "C": "Quá độ gián tiếp không cần phát triển lực lượng sản xuất.",
            "D": "Quá độ trực tiếp bỏ qua giai đoạn phát triển đại công nghiệp."
        },
        "correct_answer": "A",
        "explanation": "Quá độ gián tiếp diễn ra ở những nước chưa trải qua chế độ tư bản chủ nghĩa phát triển lên CNXH."
    },
    127: {
        "question": "Đặc trưng nổi bật của văn hóa xã hội chủ nghĩa là gì?",
        "options": {
            "A": "Xây dựng con người mới phát triển toàn diện và mang tính nhân văn sâu sắc.",
            "B": "Phục vụ cho lợi ích độc quyền của giai cấp thống trị tư sản.",
            "C": "Tách rời khỏi các giá trị tinh thần truyền thống của dân tộc.",
            "D": "Đề cao lối sống tự do cá nhân chủ nghĩa tuyệt đối."
        },
        "correct_answer": "A",
        "explanation": "Nền văn hóa XHCN giải phóng con người, xây dựng con người phát triển toàn diện."
    },
    129: {
        "question": "Động lực chủ yếu thúc đẩy sự phát triển của xã hội Việt Nam trong thời kỳ quá độ lên CNXH là gì?",
        "options": {
            "A": "Đại đoàn kết toàn dân tộc trên cơ sở liên minh công - nông - trí thức dưới sự lãnh đạo của Đảng.",
            "B": "Sự cạnh tranh gay gắt giữa các thành phần kinh tế.",
            "C": "Sự hỗ trợ viện trợ từ nước ngoài.",
            "D": "Sự tích tụ vốn tư bản của các doanh nghiệp tư nhân."
        },
        "correct_answer": "A",
        "explanation": "Khối đại đoàn kết toàn dân tộc là động lực chủ yếu để phát triển đất nước trong thời kỳ quá độ."
    },

    # --- CHAPTER 4 REPLACEMENTS (8 questions: 137, 145, 155, 157, 159, 162, 164, 175) ---
    137: {
        "question": "Nền dân chủ xã hội chủ nghĩa đầu tiên trong lịch sử được xác lập sau sự kiện lịch sử nào?",
        "options": {
            "A": "Cách mạng Tháng Mười Nga năm 1917.",
            "B": "Cách mạng Pháp năm 1789.",
            "C": "Công社 Paris năm 1871.",
            "D": "Cách mạng Tháng Tám năm 1945 ở Việt Nam."
        },
        "correct_answer": "A",
        "explanation": "Cách mạng Tháng Mười Nga 1917 khai sinh ra nhà nước xô viết và nền dân chủ XHCN đầu tiên."
    },
    145: {
        "question": "Bản chất kinh tế của nền dân chủ xã hội chủ nghĩa dựa trên chế độ sở hữu nào?",
        "options": {
            "A": "Chế độ công hữu về các tư liệu sản xuất chủ yếu.",
            "B": "Chế độ tư hữu tư bản chủ nghĩa.",
            "C": "Chế độ sở hữu phong kiến về đất đai.",
            "D": "Chế độ sở hữu độc quyền của tư bản nước ngoài."
        },
        "correct_answer": "A",
        "explanation": "Dân chủ XHCN dựa trên chế độ công hữu về TLSX chủ yếu."
    },
    155: {
        "question": "Sự khác biệt về bản chất giữa nhà nước XHCN và các nhà nước bóc lột trong lịch sử là gì?",
        "options": {
            "A": "Nhà nước XHCN là nhà nước của đại đa số nhân dân lao động trấn áp thiểu số áp bức.",
            "B": "Nhà nước XHCN không sử dụng bất kỳ công cụ pháp luật nào.",
            "C": "Nhà nước XHCN duy trì sự thống trị độc tôn của giai cấp tư sản.",
            "D": "Nhà nước XHCN là nhà nước phi giai cấp từ khi mới thành lập."
        },
        "correct_answer": "A",
        "explanation": "Nhà nước XHCN đại diện cho đại đa số quần chúng nhân dân lao động."
    },
    157: {
        "question": "Hình thức dân chủ trực tiếp ở Việt Nam được thực hiện thông qua cơ chế nào?",
        "options": {
            "A": "Nhân dân bầu cử, trưng cầu ý kiến và thực hiện quyền tự ứng cử.",
            "B": "Ủy quyền toàn bộ cho đại biểu Quốc hội quyết định thay.",
            "C": "Thông qua quyết định của các tập đoàn kinh tế tư nhân.",
            "D": "Thực hiện theo sự phân công của tổ chức quốc tế."
        },
        "correct_answer": "A",
        "explanation": "Dân chủ trực tiếp thể hiện qua bầu cử, ứng cử và trưng cầu ý dân."
    },
    159: {
        "question": "Nhà nước pháp quyền xã hội chủ nghĩa Việt Nam mang bản chất của giai cấp nào?",
        "options": {
            "A": "Giai cấp công nhân.",
            "B": "Giai cấp nông dân.",
            "C": "Tầng lớp trí thức.",
            "D": "Giai cấp tư sản dân tộc."
        },
        "correct_answer": "A",
        "explanation": "Nhà nước pháp quyền XHCN Việt Nam mang bản chất giai cấp công nhân."
    },
    162: {
        "question": "Chức năng quan trọng nhất của Nhà nước xã hội chủ nghĩa là gì?",
        "options": {
            "A": "Chức năng tổ chức, xây dựng xã hội mới.",
            "B": "Chức năng trấn áp quân sự.",
            "C": "Chức năng thu thuế và quản lý tài chính.",
            "D": "Chức năng đối ngoại ngoại giao."
        },
        "correct_answer": "A",
        "explanation": "Tổ chức và xây dựng xã hội mới là chức năng căn bản và quan trọng nhất của nhà nước XHCN."
    },
    164: {
        "question": "Trong hệ thống chính trị xã hội chủ nghĩa ở Việt Nam, tổ chức nào giữ vai trò lãnh đạo?",
        "options": {
            "A": "Đảng Cộng sản Việt Nam.",
            "B": "Mặt trận Tổ quốc Việt Nam.",
            "C": "Tổng Liên đoàn Lao động Việt Nam.",
            "D": "Hội Liên hiệp Thanh niên Việt Nam."
        },
        "correct_answer": "A",
        "explanation": "Đảng Cộng sản Việt Nam là lực lượng lãnh đạo Nhà nước và xã hội."
    },
    175: {
        "question": "Dân chủ gián tiếp (dân chủ đại diện) được thực hiện như thế nào?",
        "options": {
            "A": "Nhân dân thực hiện quyền lực thông qua đại biểu do mình bầu ra.",
            "B": "Nhân dân trực tiếp tham gia bỏ phiếu quyết định mọi chính sách.",
            "C": "Quyền lực được trao cho bộ máy chính quyền không qua bầu cử.",
            "D": "Cá nhân tự do đưa ra quyết định mà không cần đại biểu."
        },
        "correct_answer": "A",
        "explanation": "Dân chủ gián tiếp là hình thức nhân dân trao quyền lực cho đại biểu Quốc hội và HĐND."
    },

    # --- CHAPTER 5 REPLACEMENTS (7 questions: 182, 183, 185, 192, 196, 200, 215) ---
    182: {
        "question": "Cơ cấu xã hội nào giữ vị trí vị trí trung tâm và quy định các cơ cấu xã hội khác?",
        "options": {
            "A": "Cơ cấu xã hội - giai cấp.",
            "B": "Cơ cấu xã hội - dân số.",
            "C": "Cơ cấu xã hội - nghề nghiệp.",
            "D": "Cơ cấu xã hội - lãnh thổ."
        },
        "correct_answer": "A",
        "explanation": "Cơ cấu xã hội - giai cấp là cơ cấu cơ bản giữ vị trí trung tâm trong hệ thống xã hội."
    },
    183: {
        "question": "Giai cấp công nhân Việt Nam trong thời kỳ quá độ có sự biến đổi như thế nào?",
        "options": {
            "A": "Tăng nhanh về số lượng, nâng cao về chất lượng và đa dạng về cơ cấu nghề nghiệp.",
            "B": "Giảm dần về số lượng và thu hẹp quy mô sản xuất.",
            "C": "Chuyển thành giai cấp làm chủ tư nhân tư bản.",
            "D": "Mất đi vai trò lãnh đạo cách mạng."
        },
        "correct_answer": "A",
        "explanation": "GCCN Việt Nam phát triển nhanh về số lượng, chất lượng và trình độ công nghệ."
    },
    185: {
        "question": "Nội dung kinh tế của liên minh công - nông - trí thức ở Việt Nam hiện nay là gì?",
        "options": {
            "A": "Hợp tác phát triển sản xuất, liên kết kinh tế giữa công nghiệp, nông nghiệp và khoa học công nghệ.",
            "B": "Hạn chế sự giao thương giữa nông thôn và thành thị.",
            "C": "Chia đều của cải xã hội không dựa trên lao động.",
            "D": "Bắt buộc nông dân phải bỏ ruộng đất vào làm công nhân."
        },
        "correct_answer": "A",
        "explanation": "Nội dung kinh tế của liên minh là sự hợp tác kinh tế, liên kết sản xuất giữa công - nông - trí thức."
    },
    192: {
        "question": "Nội dung chính trị của liên minh giai cấp ở Việt Nam nhằm mục đích gì?",
        "options": {
            "A": "Giữ vững độc lập dân tộc và định hướng xã hội chủ nghĩa dưới sự lãnh đạo của Đảng.",
            "B": "Tạo ra sự cạnh tranh vị thế chính trị giữa các tầng lớp.",
            "C": "Bảo vệ lợi ích riêng biệt của từng giai cấp.",
            "D": "Xóa bỏ bộ máy chính quyền nhà nước."
        },
        "correct_answer": "A",
        "explanation": "Nội dung chính trị nhằm giữ vững vai trò lãnh đạo của Đảng và định hướng XHCN."
    },
    196: {
        "question": "Tầng lớp trí thức Việt Nam có vai trò đặc biệt gì trong thời kỳ quá độ?",
        "options": {
            "A": "Là lực lượng lao động sáng tạo đặc biệt trong phát triển kinh tế tri thức và đổi mới sáng tạo.",
            "B": "Là giai cấp lãnh đạo độc lập nền kinh tế.",
            "C": "Là lực lượng trực tiếp sản xuất nông sản.",
            "D": "Là tập đoàn nắm giữ tư liệu sản xuất tư nhân."
        },
        "correct_answer": "A",
        "explanation": "Trí thức là lực lượng lao động sáng tạo quan trọng trong thời đại kinh tế tri thức."
    },
    200: {
        "question": "Nội dung văn hóa - xã hội của liên minh công - nông - trí thức là gì?",
        "options": {
            "A": "Xây dựng nền văn hóa tiên tiến, đậm đà bản sắc dân tộc, nâng cao dân trí và phúc lợi xã hội.",
            "B": "Đồng hóa văn hóa giữa các vùng miền.",
            "C": "Thương mại hóa toàn bộ các hoạt động giáo dục y tế.",
            "D": "Giảm bớt các chi tiêu đầu tư cho giáo dục đào tạo."
        },
        "correct_answer": "A",
        "explanation": "Nội dung văn hóa xã hội của liên minh tập trung nâng cao đời sống tinh thần và dân trí."
    },
    215: {
        "question": "Xu hướng biến đổi của giai cấp nông dân Việt Nam hiện nay là gì?",
        "options": {
            "A": "Giảm dần về tỷ lệ trong cơ cấu lao động và phân hóa thành các bộ phận lao động mới.",
            "B": "Tăng nhanh tỷ lệ chi phối toàn bộ nền kinh tế.",
            "C": "Giữ nguyên mô hình canh tác tiểu nông truyền thống.",
            "D": "Chuyển toàn bộ thành tầng lớp tư sản nông nghiệp."
        },
        "correct_answer": "A",
        "explanation": "Tỷ lệ lao động nông nghiệp và nông dân giảm dần do quá trình công nghiệp hóa."
    },

    # --- CHAPTER 6 REPLACEMENTS (18 questions: 262, 263, 264, 266, 269, 270, 271, 272, 273, 276, 277, 278, 280, 281, 285, 294, 295, 297) ---
    262: {
        "question": "Theo V.I. Lênin, hai xu hướng khách quan trong sự phát triển của quan hệ dân tộc là gì?",
        "options": {
            "A": "Tách ra để thành lập các quốc gia dân tộc độc lập và xích lại gần nhau để liên hiệp hợp tác.",
            "B": "Đồng hóa dân tộc nhỏ và thôn tính lãnh thổ.",
            "C": "Phân chia giai cấp và xung đột sắc tộc.",
            "D": "Đóng cửa biên giới và cấm đoán giao lưu văn hóa."
        },
        "correct_answer": "A",
        "explanation": "Hai xu hướng dân tộc: Tách ra thành lập quốc gia độc lập và xích lại gần nhau hợp tác."
    },
    263: {
        "question": "Nội dung quan trọng nhất trong Cương lĩnh dân tộc của V.I. Lênin là gì?",
        "options": {
            "A": "Các dân tộc hoàn toàn bình đẳng, các dân tộc được quyền tự quyết, liên hiệp công nhân tất cả các dân tộc.",
            "B": "Ưu tiên quyền lợi cho dân tộc đa số.",
            "C": "Đề cao chủ nghĩa dân tộc hẹp hòi.",
            "D": "Xóa bỏ ngôn ngữ và văn hóa dân tộc thiểu số."
        },
        "correct_answer": "A",
        "explanation": "Ba nội dung Cương lĩnh dân tộc Lênin: Bình đẳng, Tự quyết, Liên hiệp công nhân các dân tộc."
    },
    264: {
        "question": "Quyền tự quyết của các dân tộc được hiểu là gì?",
        "options": {
            "A": "Quyền tự lựa chọn chế độ chính trị và con đường phát triển của dân tộc mình.",
            "B": "Quyền tự do ly khai bất kỳ lúc nào không cần căn cứ.",
            "C": "Quyền can thiệp vào công việc nội bộ quốc gia khác.",
            "D": "Quyền từ chối các điều ước quốc tế về nhân quyền."
        },
        "correct_answer": "A",
        "explanation": "Quyền tự quyết là quyền tự định đoạt vận mệnh chính trị và con đường phát triển."
    },
    266: {
        "question": "Bản chất của tôn giáo theo quan điểm của chủ nghĩa Mác - Lênin là gì?",
        "options": {
            "A": "Là một hình thái ý thức xã hội phản ánh hư ảo thực tại khách quan.",
            "B": "Là nguồn gốc chân lý tuyệt đối của tự nhiên.",
            "C": "Là hiện tượng siêu tự nhiên có trước thế giới vật chất.",
            "D": "Là hệ tư tưởng duy nhất chỉ đạo khoa học hiện đại."
        },
        "correct_answer": "A",
        "explanation": "Tôn giáo là một hình thái ý thức xã hội phản ánh hoang đường, hư ảo thực tại khách quan."
    },
    269: {
        "question": "Nguyên nhân kinh tế dẫn đến sự tồn tại của tôn giáo trong thời kỳ quá độ là gì?",
        "options": {
            "A": "Sự tồn tại của nền kinh tế nhiều thành phần và bất trắc trong sản xuất kinh doanh.",
            "B": "Sự phát triển vượt bậc của khoa học kỹ thuật.",
            "C": "Sự xóa bỏ hoàn toàn chế độ tư hữu.",
            "D": "Sự biến mất của nền kinh tế thị trường."
        },
        "correct_answer": "A",
        "explanation": "Kinh tế nhiều thành phần và rủi ro kinh doanh khiến con người tìm sự an ủi tôn giáo."
    },
    270: {
        "question": "Nguyên nhân tâm lý dẫn đến sự tồn tại của tôn giáo là gì?",
        "options": {
            "A": "Sự sợ hãi, bế tắc của con người trước sức mạnh tự nhiên và rủi ro xã hội.",
            "B": "Tính kiên định lý trí của nhà khoa học.",
            "C": "Sự gia tăng thu nhập và mức sống.",
            "D": "Khả năng làm chủ hoàn toàn tự nhiên của con người."
        },
        "correct_answer": "A",
        "explanation": "Tâm lý lo âu, sợ hãi trước thiên tai, tai họa làm tôn giáo duy trì chốn an ủi tâm linh."
    },
    271: {
        "question": "Nguyên tắc cốt lõi trong giải quyết vấn đề tôn giáo của Đảng và Nhà nước ta là gì?",
        "options": {
            "A": "Tín ngưỡng, tôn giáo là nhu cầu tinh thần của một bộ phận nhân dân; thực hiện tự do tín ngưỡng.",
            "B": "Cấm đoán mọi hoạt động tôn giáo công khai.",
            "C": "Bắt buộc mọi người dân phải theo một tôn giáo nhất định.",
            "D": "Thương mại hóa các cơ sở thờ tự tôn giáo."
        },
        "correct_answer": "A",
        "explanation": "Tôn giáo là nhu cầu tinh thần của một bộ phận nhân dân, Nhà nước tôn trọng tự do tín ngưỡng."
    },
    272: {
        "question": "Đặc điểm nổi bật của các dân tộc thiểu số ở Việt Nam là gì?",
        "options": {
            "A": "Cư trú xen kẽ, phân bố rộng lớn trên các địa bàn chiến lược về quốc phòng an ninh.",
            "B": "Sống tập trung biệt lập hoàn toàn ở các đảo xa.",
            "C": "Chiếm đại đa số dân số cả nước.",
            "D": "Có trình độ phát triển đồng đều như dân tộc đa số."
        },
        "correct_answer": "A",
        "explanation": "Các dân tộc thiểu số ở Việt Nam cư trú xen kẽ trên các vị trí địa chính trị chiến lược."
    },
    273: {
        "question": "Chính sách dân tộc cơ bản của Đảng Cộng sản Việt Nam là:",
        "options": {
            "A": "Bình đẳng, đoàn kết, tôn trọng và giúp nhau cùng phát triển.",
            "B": "Đồng hóa văn hóa các dân tộc ít người.",
            "C": "Phân chia khu vực tự trị khép kín.",
            "D": "Ưu tiên phát triển riêng vùng đô thị."
        },
        "correct_answer": "A",
        "explanation": "Chính sách dân tộc xuyên suốt là Bình đẳng, đoàn kết, tương trợ giúp nhau cùng phát triển."
    },
    276: {
        "question": "Tính chất lịch sử của tôn giáo thể hiện ở điểm nào?",
        "options": {
            "A": "Tôn giáo có sự hình thành, phát triển và sẽ biến mất khi các điều kiện tồn tại của nó không còn.",
            "B": "Tôn giáo tồn tại vĩnh viễn không bao giờ thay đổi.",
            "C": "Tôn giáo ra đời cùng lúc với sự xuất hiện của Trái Đất.",
            "D": "Tôn giáo không chịu sự tác động của các hình thái kinh tế."
        },
        "correct_answer": "A",
        "explanation": "Tôn giáo có tính lịch sử, nó xuất hiện có điều kiện và sẽ tiêu vong khi điều kiện đó mất đi."
    },
    277: {
        "question": "Tính quần chúng của tôn giáo thể hiện ở chỗ:",
        "options": {
            "A": "Tôn giáo là nơi sinh hoạt văn hóa tinh thần của đông đảo quần chúng nhân dân.",
            "B": "Tôn giáo chỉ dành riêng cho tầng lớp thượng lưu.",
            "C": "Tôn giáo quy định toàn bộ pháp luật của nhà nước.",
            "D": "Tôn giáo không thu hút sự tham gia của nhân dân."
        },
        "correct_answer": "A",
        "explanation": "Tính quần chúng biểu hiện ở số lượng tín đồ đông đảo và giá trị đạo đức hướng thiện."
    },
    278: {
        "question": "Nguồn gốc nhận thức của tôn giáo là gì?",
        "options": {
            "A": "Nhận thức của con người về tự nhiên và xã hội còn hạn chế, tuyệt đối hóa mặt chủ quan.",
            "B": "Sự hiểu biết hoàn hảo về quy luật vũ trụ.",
            "C": "Khả năng dự báo chính xác tương lai của khoa học.",
            "D": "Sự hoàn thiện của tri thức toán học."
        },
        "correct_answer": "A",
        "explanation": "Nguồn gốc nhận thức là do giới hạn hiểu biết của con người trước tự nhiên phức tạp."
    },
    280: {
        "question": "Phân biệt hai mặt chính trị và tư tưởng trong giải quyết vấn đề tôn giáo nhằm mục đích gì?",
        "options": {
            "A": "Tránh cực đoan: không quy mọi tín đồ thành kẻ thù chính trị và không buông lỏng cảnh giác với kẻ lợi dụng tôn giáo.",
            "B": "Loại bỏ hoàn toàn tín đồ tôn giáo ra khỏi xã hội.",
            "C": "Cấm đoán mọi hoạt động tín ngưỡng.",
            "D": "Bỏ qua các hành vi vi phạm pháp luật núp bóng tôn giáo."
        },
        "correct_answer": "A",
        "explanation": "Mặt tư tưởng giải quyết bằng giáo dục; mặt chính trị đấu tranh chống lợi dụng tôn giáo phá hoại."
    },
    281: {
        "question": "Một trong những yếu tố tạo nên sự đoàn kết dân tộc ở Việt Nam là gì?",
        "options": {
            "A": "Truyền thống yêu nước và lịch sử chung sức chống ngoại xâm, thiên tai.",
            "B": "Sự đồng nhất hoàn toàn về ngôn ngữ nói.",
            "C": "Sự giống nhau tuyệt đối về phong tục tập quán.",
            "D": "Sự chia rẽ vùng miền địa lý."
        },
        "correct_answer": "A",
        "explanation": "Truyền thống yêu nước dựng nước và giữ nước đúc kết nên khối đại đoàn kết dân tộc Việt Nam."
    },
    285: {
        "question": "Nội dung quan trọng nhất trong việc thực hiện quyền bình đẳng dân tộc ở Việt Nam là:",
        "options": {
            "A": "Đảm bảo bình đẳng về chính trị, kinh tế, văn hóa, xã hội giữa các dân tộc.",
            "B": "Chỉ phát triển kinh tế cho dân tộc thiểu số.",
            "C": "Ưu tiên tuyển dụng không căn cứ vào năng lực.",
            "D": "Xóa bỏ các di sản văn hóa riêng."
        },
        "correct_answer": "A",
        "explanation": "Bình đẳng dân tộc phải thể hiện trên tất cả các lĩnh vực chính trị, kinh tế, văn hóa, xã hội."
    },
    294: {
        "question": "Thực chất của việc giải quyết vấn đề tôn giáo trong thời kỳ quá độ là gì?",
        "options": {
            "A": "Khắc phục dần những ảnh hưởng tiêu cực của tôn giáo gắn liền với cải tạo xã hội cũ, xây dựng xã hội mới.",
            "B": "Dùng biện pháp hành chính cưỡng chế xóa bỏ tôn giáo ngay lập tức.",
            "C": "Khuyến khích phát triển mê tín dị đoan.",
            "D": "Xem tôn giáo là lực lượng lãnh đạo xã hội."
        },
        "correct_answer": "A",
        "explanation": "Giải quyết vấn đề tôn giáo là quá trình lâu dài gắn liền với xây dựng CNXH nâng cao đời sống."
    },
    295: {
        "question": "Thế giời quan tôn giáo khác thế giới quan Mác - Lênin ở điểm căn bản nào?",
        "options": {
            "A": "Thế giới quan tôn giáo là duy tâm, thế giới quan Mác - Lênin là duy vật phiếm thần/duy vật duy sinh.",
            "B": "Thế giới quan tôn giáo hoàn toàn khoa học.",
            "C": "Thế giới quan Mác - Lênin thừa nhận thần linh cai trị.",
            "D": "Cả hai thế giới quan đều phản ánh đúng bản chất tự nhiên."
        },
        "correct_answer": "A",
        "explanation": "Thế giới quan Mác - Lênin duy vật khoa học; thế giới quan tôn giáo mang tính duy tâm."
    },
    297: {
        "question": "Tại sao giải quyết vấn đề tôn giáo phải có quan điểm lịch sử cụ thể?",
        "options": {
            "A": "Vì vai trò và thái độ chính trị của tôn giáo thay đổi theo từng giai đoạn lịch sử.",
            "B": "Vì tôn giáo không bao giờ có sự thay đổi.",
            "C": "Vì các giáo lý tôn giáo luôn giống nhau qua mọi thời đại.",
            "D": "Vì chính sách nhà nước không cần điều chỉnh."
        },
        "correct_answer": "A",
        "explanation": "Ở mỗi thời kỳ lịch sử, vai trò của giáo hội và tín đồ có sự khác nhau nên cần ứng xử linh hoạt."
    },

    # --- CHAPTER 7 REPLACEMENTS (24 questions: 217, 219, 221, 223, 226, 227, 228, 229, 230, 231, 238, 243, 244, 245, 246, 248, 249, 251, 252, 253, 254, 255, 256, 258) ---
    217: {
        "question": "Gia đình là một hình thái xã hội đặc biệt được hình thành và phát triển dựa trên hai mối quan hệ cơ bản nào?",
        "options": {
            "A": "Quan hệ hôn nhân và quan hệ huyết thống.",
            "B": "Quan hệ kinh tế và quan hệ chính trị.",
            "C": "Quan hệ bạn bè và quan hệ đồng nghiệp.",
            "D": "Quan hệ xóm giềng và quan hệ huyết thống."
        },
        "correct_answer": "A",
        "explanation": "Hôn nhân và huyết thống là hai mối quan hệ nền tảng cấu thành gia đình."
    },
    219: {
        "question": "Chức năng nào được coi là chức năng đặc thù và riêng có của gia đình?",
        "options": {
            "A": "Tái sản xuất ra con người.",
            "B": "Quản lý kinh tế nhà nước.",
            "C": "Bảo vệ an ninh quốc phòng.",
            "D": "Cung cấp giáo dục đại học."
        },
        "correct_answer": "A",
        "explanation": "Tái sản xuất ra con người để duy trì nòi giống là chức năng riêng có của gia đình."
    },
    221: {
        "question": "Nội dung nào sau đây phản ánh đúng vị trí của gia đình đối với xã hội?",
        "options": {
            "A": "Gia đình là tế bào của xã hội.",
            "B": "Gia đình độc lập hoàn toàn không chịu tác động của xã hội.",
            "C": "Gia đình quyết định toàn bộ bản chất của kiến trúc thượng tầng.",
            "D": "Gia đình chỉ xuất hiện ở chế độ tư bản chủ nghĩa."
        },
        "correct_answer": "A",
        "explanation": "Gia đình là tế bào của xã hội, xã hội tốt đẹp thì gia đình tốt đẹp."
    },
    223: {
        "question": "Chế độ hôn nhân tiến bộ trong chủ nghĩa xã hội dựa trên nguyên tắc cơ bản nào?",
        "options": {
            "A": "Hôn nhân tự nguyện, một vợ một chồng, vợ chồng bình đẳng.",
            "B": "Hôn nhân do cha mẹ đặt đâu ngồi đó.",
            "C": "Hôn nhân đa thê theo tập quán cổ xưa.",
            "D": "Hôn nhân gượng ép vì lợi ích tài sản."
        },
        "correct_answer": "A",
        "explanation": "Hôn nhân tiến bộ dựa trên sự tự nguyện, một vợ một chồng và bình đẳng nam nữ."
    },
    226: {
        "question": "Cơ sở kinh tế - xã hội để xây dựng gia đình mới trong thời kỳ quá độ lên CNXH là gì?",
        "options": {
            "A": "Xác lập chế độ công hữu về tư liệu sản xuất và phát triển kinh tế XHCN.",
            "B": "Duy trì chế độ tư hữu tư bản chủ nghĩa.",
            "C": "Tăng cường tích tụ tài sản cá nhân.",
            "D": "Xóa bỏ hoàn toàn thu nhập lao động."
        },
        "correct_answer": "A",
        "explanation": "Chế độ công hữu về TLSX giải phóng người phụ nữ và tạo cơ sở bình đẳng gia đình."
    },
    227: {
        "question": "Chức năng kinh tế và tổ chức tiêu dùng của gia đình ở Việt Nam hiện nay có sự biến đổi như thế nào?",
        "options": {
            "A": "Từ đơn vị tiêu dùng chuyển thành đơn vị sản xuất hàng hóa và dịch vụ đa dạng.",
            "B": "Hoàn toàn mất đi chức năng kinh tế.",
            "C": "Chỉ còn chức năng tiêu dùng tự cấp tự túc.",
            "D": "Do nhà nước đảm nhiệm toàn bộ."
        },
        "correct_answer": "A",
        "explanation": "Gia đình hiện nay là đơn vị kinh tế tự chủ, sản xuất kinh doanh hàng hóa dịch vụ."
    },
    228: {
        "question": "Sự biến đổi về quy mô gia đình Việt Nam trong thời kỳ hiện đại theo xu hướng nào?",
        "options": {
            "A": "Quy mô gia đình thu nhỏ lại (mô hình gia đình hạt nhân chiếm ưu thế).",
            "B": "Gia đình đại gia đình nhiều thế hệ tăng nhanh.",
            "C": "Gia đình tập thể quy mô lớn.",
            "D": "Không có sự thay đổi quy mô."
        },
        "correct_answer": "A",
        "explanation": "Gia đình hạt nhân (cha mẹ và con cái) ngày càng trở nên phổ biến thay cho gia đình tam đại đồng đường."
    },
    229: {
        "question": "Yếu tố chính trị - xã hội quyết định sự bình đẳng nam nữ trong gia đình là gì?",
        "options": {
            "A": "Thiết lập chính quyền của nhân dân lao động và hệ thống pháp luật XHCN.",
            "B": "Thói quen phong kiến truyền thống.",
            "C": "Sự gia tăng phân hóa giàu nghèo.",
            "D": "Tập quán sinh con trai nối dỗi."
        },
        "correct_answer": "A",
        "explanation": "Nhà nước XHCN và hệ thống pháp luật bảo đảm quyền bình đẳng nam nữ."
    },
    230: {
        "question": "Chức năng nuôi dưỡng, giáo dục con cái của gia đình có vai trò gì đối với xã hội?",
        "options": {
            "A": "Hình thành nhân cách, đạo đức và tri thức cho thế hệ trẻ.",
            "B": "Cung cấp nguồn thu nhập trực tiếp cho ngân sách.",
            "C": "Thay thế hoàn toàn vai trò của nhà trường.",
            "D": "Giảm bớt trách nhiệm pháp lý của cha mẹ."
        },
        "correct_answer": "A",
        "explanation": "Gia đình là môi trường đầu tiên hình thành và giáo dục nhân cách con người."
    },
    231: {
        "question": "Mối quan hệ giữa gia đình và xã hội là mối quan hệ như thế nào?",
        "options": {
            "A": "Mối quan hệ tác động qua lại lẫn nhau; xã hội quyết định gia đình và gia đình thúc đẩy xã hội.",
            "B": "Mối quan hệ một chiều từ gia đình đến xã hội.",
            "C": "Mối quan hệ tách biệt không liên quan.",
            "D": "Gia đình quyết định tuyệt đối sự tồn tại của xã hội."
        },
        "correct_answer": "A",
        "explanation": "Xã hội quy định sự biến đổi của gia đình, ngược lại gia đình góp phần ổn định xã hội."
    },
    238: {
        "question": "Nội dung nào sau đây thể hiện sự biến đổi trong mối quan hệ giữa các thế hệ trong gia đình hiện đại?",
        "options": {
            "A": "Mối quan hệ trở nên bình đẳng, dân chủ hơn nhưng thách thức việc giữ gìn sự gắn kết.",
            "B": "Sự phục tùng tuyệt đối mang tính gia trưởng độc đoán.",
            "C": "Con cái không còn bất kỳ trách nhiệm nào với cha mẹ.",
            "D": "Cha mẹ áp đặt toàn bộ quyết định hôn nhân của con."
        },
        "correct_answer": "A",
        "explanation": "Gia đình hiện đại đề cao tính bình đẳng, dân chủ và tôn trọng ý kiến cá nhân."
    },
    243: {
        "question": "Phương hướng xây dựng gia đình Việt Nam trong thời kỳ quá độ lên CNXH là:",
        "options": {
            "A": "Xây dựng gia đình no ấm, bình đẳng, tiến bộ, hạnh phúc.",
            "B": "Quay trở lại mô hình gia đình phong kiến cổ xưa.",
            "C": "Tây hóa hoàn toàn lối sống gia đình.",
            "D": "Xóa bỏ thiết chế gia đình trong xã hội."
        },
        "correct_answer": "A",
        "explanation": "Mục tiêu xây dựng gia đình Việt Nam là No ấm, bình đẳng, tiến bộ, hạnh phúc."
    },
    244: {
        "question": "Quan hệ nuôi dưỡng, chăm sóc giữa các thành viên trong gia đình biểu hiện trách nhiệm gì?",
        "options": {
            "A": "Trách nhiệm tình cảm, đạo đức và pháp lý giữa các thành viên.",
            "B": "Trách nhiệm hợp đồng kinh tế đơn thuần.",
            "C": "Trách nhiệm hành chính với chính quyền địa phương.",
            "D": "Sự trao đổi thương mại tài chính."
        },
        "correct_answer": "A",
        "explanation": "Nuôi dưỡng chăm sóc vừa là nghĩa vụ đạo đức thiêng liêng vừa là trách nhiệm pháp lý."
    },
    245: {
        "question": "Vì sao công nghiệp hóa, hiện đại hóa làm thay đổi cấu trúc gia đình?",
        "options": {
            "A": "Vì nó làm dịch chuyển lao động, tăng tính di động xã hội và tạo việc làm mới.",
            "B": "Vì nó cấm đoán các gia đình sống chung.",
            "C": "Vì nó làm giảm thu nhập của người lao động.",
            "D": "Vì nó buộc phụ nữ phải nghỉ việc ở nhà."
        },
        "correct_answer": "A",
        "explanation": "Quá trình CNH, HNH tạo sự di động lao động làm thay đổi quy mô và cấu trúc gia đình."
    },
    246: {
        "question": "Trách nhiệm của Nhà nước trong việc bảo vệ gia đình là gì?",
        "options": {
            "A": "Ban hành Luật Hôn nhân & Gia đình và các chính sách an sinh xã hội hỗ trợ gia đình.",
            "B": "Can thiệp vào nội dung sinh hoạt riêng tư của từng gia đình.",
            "C": "Bắt buộc các gia đình phải sinh số con theo ấn định cứng nhắc.",
            "D": "Loại bỏ hỗ trợ y tế giáo dục gia đình."
        },
        "correct_answer": "A",
        "explanation": "Nhà nước bảo vệ gia đình thông qua hệ thống luật pháp và chính sách an sinh."
    },
    248: {
        "question": "Sự biến đổi của chức năng thỏa mãn nhu cầu tâm sinh lý, duy trì tình cảm gia đình hiện nay có xu hướng:",
        "options": {
            "A": "Ngày càng gia tăng và đóng vai trò yếu tố cốt lõi giữ gìn sự bền vững gia đình.",
            "B": "Giảm bớt vai trò và không còn quan trọng.",
            "C": "Chuyển giao toàn bộ cho các tổ chức xã hội.",
            "D": "Bị thay thế hoàn toàn bởi các quan hệ bạn bè."
        },
        "correct_answer": "A",
        "explanation": "Gia đình hiện đại chú trọng yếu tố tình cảm, chia sẻ tâm lý và nâng cao chất lượng cuộc sống."
    },
    249: {
        "question": "Mối quan hệ giữa vợ và chồng trong gia đình XHCN được xây dựng trên nền tảng nào?",
        "options": {
            "A": "Tình yêu thương chân chính, sự thủy chung, tôn trọng và bình đẳng.",
            "B": "Sự tính toán giá trị tài sản cá nhân.",
            "C": "Sự áp đặt gia trưởng của người chồng.",
            "D": "Sự phụ thuộc kinh tế hoàn toàn của người vợ."
        },
        "correct_answer": "A",
        "explanation": "Tình yêu thương, thủy chung và bình đẳng là nền tảng bền vững của quan hệ vợ chồng."
    },
    251: {
        "question": "Biến đổi trong chức năng giáo dục của gia đình Việt Nam hiện nay là gì?",
        "options": {
            "A": "Sự kết hợp chặt chẽ giữa giáo dục gia đình, giáo dục nhà trường và giáo dục xã hội.",
            "B": "Phó mặc hoàn toàn cho nhà trường giáo dục.",
            "C": "Gia đình tự giáo dục không tuân theo chương trình chung.",
            "D": "Xóa bỏ các bài học đạo đức truyền thống."
        },
        "correct_answer": "A",
        "explanation": "Giáo dục gia đình kết hợp gắn bó với nhà trường và xã hội để phát triển nhân cách."
    },
    252: {
        "question": "Khái niệm 'Gia đình hạt nhân' được hiểu là gì?",
        "options": {
            "A": "Gia đình bao gồm hai thế hệ: bố mẹ và con cái chưa kết hôn.",
            "B": "Gia đình từ ba thế hệ trở lên cùng sinh sống.",
            "C": "Gia đình chỉ có một người sinh sống duy nhất.",
            "D": "Gia đình tập hợp các dòng họ."
        },
        "correct_answer": "A",
        "explanation": "Gia đình hạt nhân là mô hình gia đình 2 thế hệ gồm cha mẹ và con cái."
    },
    253: {
        "question": "Tác động tích cực của kinh tế thị trường đối với gia đình ở Việt Nam là gì?",
        "options": {
            "A": "Tạo điều kiện tăng thu nhập, nâng cao mức sống và đa dạng hóa cơ hội nghề nghiệp.",
            "B": "Làm phai nhạt tình cảm dòng họ.",
            "C": "Gia tăng áp lực ly hôn.",
            "D": "Tạo ra lối sống sùng bái tiền tài."
        },
        "correct_answer": "A",
        "explanation": "Kinh tế thị trường giúp nâng cao thu nhập, cải thiện điều kiện sống cho các gia đình."
    },
    254: {
        "question": "Vấn đề nào đang là thách thức đối với việc giữ gìn sự bền vững gia đình ở Việt Nam hiện nay?",
        "options": {
            "A": "Tỷ lệ ly hôn tăng, bạo lực gia đình và lối sống thực dụng gia tăng.",
            "B": "Mức sống gia đình ngày càng cao.",
            "C": "Trình độ học vấn của các thành viên được nâng lên.",
            "D": "Chính sách hỗ trợ gia đình của Nhà nước."
        },
        "correct_answer": "A",
        "explanation": "Tác động mặt trái kinh tế thị trường nảy sinh thách thức về ly hôn, lối sống cá nhân."
    },
    255: {
        "question": "Tại sao việc giải phóng phụ nữ là điều kiện bắt buộc để xây dựng gia đình XHCN?",
        "options": {
            "A": "Vì người phụ nữ chiếm một nửa lực lượng lao động và có vai trò trung tâm trong gia đình.",
            "B": "Vì người phụ nữ nắm giữ toàn bộ chính quyền nhà nước.",
            "C": "Vì nam giới không muốn tham gia công việc nhà.",
            "D": "Vì đây là yêu cầu từ các tổ chức quốc tế."
        },
        "correct_answer": "A",
        "explanation": "Giải phóng phụ nữ là thước đo mức độ giải phóng xã hội và xây dựng gia đình bình đẳng."
    },
    256: {
        "question": "Bình đẳng giữa các thế hệ trong gia đình được hiểu là:",
        "options": {
            "A": "Cha mẹ tôn trọng ý kiến con cái, con cái hiếu thảo chăm sóc cha mẹ.",
            "B": "Con cái được tự do làm mọi việc không cần hỏi ý kiến cha mẹ.",
            "C": "Cha mẹ áp đặt toàn bộ tương lai nghề nghiệp của con.",
            "D": "Các thế hệ không sống chung dưới một mái nhà."
        },
        "correct_answer": "A",
        "explanation": "Bình đẳng thế hệ dựa trên sự tôn trọng lắng nghe và tình thương yêu hiếu thảo."
    },
    258: {
        "question": "Mục tiêu tiêu biểu nhất của Ngày Gia đình Việt Nam (28/6) hàng năm là gì?",
        "options": {
            "A": "Tôn vinh các giá trị văn hóa gia đình truyền thống và nâng cao ý thức xây dựng gia đình hạnh phúc.",
            "B": "Khuyến khích các gia đình đi du lịch nước ngoài.",
            "C": "Tăng cường thu thuế hộ gia đình.",
            "D": "Tổ chức các cuộc thi kinh doanh hộ gia đình."
        },
        "correct_answer": "A",
        "explanation": "Ngày Gia đình Việt Nam 28/6 tôn vinh mái ấm gia đình, lan tỏa thông điệp gia đình no ấm hạnh phúc."
    }
}

def main():
    json_path = 'data/cnxhkh_vhu.json'
    print(f"Loading {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data['questions']
    print(f"Original questions count: {len(questions)}")

    replaced_count = 0
    for q in questions:
        qid = q['id']
        if qid in REPLACEMENTS:
            rep = REPLACEMENTS[qid]
            q['question'] = rep['question']
            q['options'] = rep['options']
            q['correct_answer'] = rep['correct_answer']
            q['explanation'] = rep['explanation']
            replaced_count += 1

    print(f"Successfully replaced {replaced_count} duplicate questions with 100% UNIQUE high quality questions!")

    # Verify uniqueness
    seen = set()
    duplicates = []
    for q in questions:
        t = q['question'].strip()
        if t in seen:
            duplicates.append(q['id'])
        seen.add(t)

    print(f"Post-replacement verification: Total Questions = {len(questions)}, Unique Questions = {len(seen)}, Duplicates = {len(duplicates)}")

    if len(duplicates) == 0:
        print("CONGRATULATIONS! 0 DUPLICATES REMAIN! ALL 300 QUESTIONS ARE 100% UNIQUE!")
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved clean dataset to {json_path}")
    else:
        print(f"WARNING: Still found {len(duplicates)} duplicates: {duplicates}")

if __name__ == '__main__':
    main()
