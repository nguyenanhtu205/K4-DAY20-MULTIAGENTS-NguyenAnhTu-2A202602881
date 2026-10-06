# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin sinh viên và cấu hình

- Họ tên: Nguyễn Anh Tú
- Mã sinh viên: 2A202602881
- Hình thức thực hiện: Bài cá nhân.

- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: Google AI Studio Gemini (`google_genai:gemini-3.5-flash`), 0, 60.
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: Deep Agents 0.7.21; Windows 10.0.26300.0; chạy trực tiếp bằng PowerShell trong virtual environment.
- Số lần chạy tác vụ đã dùng / ngân sách: 1 / tối đa 30 lần chạy khuyến nghị. Lần `baseline` của `code-learn` bị Gemini trả `429 RESOURCE_EXHAUSTED` sau 199,7 giây, nên không dùng làm bằng chứng lỗi tác tử.
- Commit của tag `freeze`: Chưa tạo. Không thực hiện commit hoặc push trong quá trình hỗ trợ này theo yêu cầu của sinh viên.

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Dự đoán `subagents` không nhất thiết tăng điểm trung bình so với `baseline` trên tác vụ đánh giá, nhưng sẽ tốn nhiều token hơn. Các tác vụ nhỏ cần giữ ngữ cảnh liên tục; subagent cô lập ngữ cảnh và phải nhận lại đầy đủ quy tắc trong lời giao việc. `02_subagents.md` cũng nêu chi phí đa tác tử thường tăng đáng kể.
- H2 (skills-auto so với baseline): Dự đoán `skills-auto` có thể cải thiện các check quy ước đã xuất hiện ở tác vụ học nếu tác tử đọc skill, nhưng lợi ích trên tác vụ đánh giá có thể nhỏ hoặc âm do quy ước mới và nguy cơ quá khớp. Căn cứ: `04_curator.md` tóm tắt SkillsBench và SkillEvolBench, đồng thời GUIDE yêu cầu tách tập học/tập đánh giá để kiểm tra chính rủi ro này.
- H3 (tác vụ học so với tác vụ đánh giá): Dự đoán điểm các tác vụ học cao hơn tác vụ đánh giá cùng điều kiện, đặc biệt ở `skills-auto`, vì curator chỉ nhận phản hồi `detail` của tác vụ học; tác vụ đánh giá thêm một quy ước không có trong phản hồi học.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử Deep Agents mặc định có các công cụ tệp `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`; công cụ shell `execute`; và công cụ subagent `task`. Công cụ cho phép chạy lệnh là `execute`.
2. `task` có subagent mặc định `general-purpose`, dùng cho các tác vụ phức tạp/nhiều bước như tìm kiếm hoặc nghiên cứu. Mỗi lần gọi là một phiên tách biệt: subagent chỉ thấy prompt mà tác tử chính gửi và trả về một báo cáo cuối; vì vậy tác tử chính phải truyền đủ yêu cầu và đường dẫn.
3. Từ mô tả `task`: “Tell the agent whether to create content, analyze, or only research”. Từ mô tả `execute`: “You MUST avoid using search commands like find and grep”; thay vào đó dùng các công cụ `glob`, `grep` và `read_file` tương ứng.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| code-learn | `tests_not_modified` | A. Bỏ qua đặc tả | Đề bài ghi “Do not modify the existing files in `tests/`”; check báo “the original files in tests/ must not be modified”. |
| code-learn | `rule_type_hints` | E. Vi phạm quy ước tổ chức | `RULE: every public function ... has type annotations on all parameters and on the return value.` |
| code-learn | `rule_regression_tests` | E. Vi phạm quy ước tổ chức | `RULE: add tests/test_regressions.py ... (at least 3)`. |
| code-learn | `rule_changelog` | E. Vi phạm quy ước tổ chức | `RULE: record each fix in CHANGELOG.md ... (at least 3 bullets)`. |
| data-learn | `rule_money_in_cents` | E. Vi phạm quy ước tổ chức | `RULE: money values in answer.json are integer cents`. |
| data-learn | `rule_meta_block` | E. Vi phạm quy ước tổ chức | `RULE: answer.json has an object meta = {...}`. |
| data-learn | `rule_clean_csv` | E. Vi phạm quy ước tổ chức | `RULE: write workspace/clean.csv ... amount in integer cents.` |
| logs-learn | `valid_structure` | G. Khác | `FileNotFoundError`: `workspace/errors.json` không được tạo; trace chỉ có hai lần đọc, không có lời gọi ghi tệp. |
| logs-learn | `entry_count` | G. Khác | Cùng nguyên nhân: thiếu `workspace/errors.json`, nên không thể kiểm tra số entry. |
| logs-learn | `timestamps_utc` | G. Khác | Cùng nguyên nhân: thiếu `workspace/errors.json`, nên không thể kiểm tra timestamp. |
| logs-learn | `exception_fields` | G. Khác | Cùng nguyên nhân: thiếu `workspace/errors.json`, nên không thể kiểm tra exception. |
| logs-learn | `repeat_counts` | G. Khác | Cùng nguyên nhân: thiếu `workspace/errors.json`, nên không thể kiểm tra repeat count. |
| logs-learn | `counts_by_service` | G. Khác | Cùng nguyên nhân: thiếu `workspace/errors.json`, nên không thể kiểm tra tổng theo service. |
| logs-learn | `rule_service_names` | G. Khác | Cùng nguyên nhân: thiếu tệp đầu ra, nên check quy ước không thể chạy có ý nghĩa. |
| logs-learn | `rule_sorted_errors` | G. Khác | Cùng nguyên nhân: thiếu tệp đầu ra, nên check quy ước không thể chạy có ý nghĩa. |
| logs-learn | `rule_schema_header` | G. Khác | Cùng nguyên nhân: thiếu tệp đầu ra, nên check quy ước không thể chạy có ý nghĩa. |

Nhận xét: 6 check có `RULE:` là nhóm E và cho thấy thiếu tri thức về quy ước Acme; đây là mục tiêu phù hợp cho curator/skill. `code-learn` vẫn đạt 6/10 và `data-learn` đạt 5/8 ở các check kỹ thuật, là bằng chứng phủ định rằng lỗi chính của hai tác vụ này không phải xử lý định dạng/dữ liệu bẩn. `logs-learn` là ngoại lệ: model kết thúc trước khi tạo tệp đầu ra; cần đối chiếu sau khi chạy lại để tách lỗi hoàn thành tác vụ khỏi nhiễu model/provider.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa: `explorer` (khảo sát yêu cầu, dữ liệu và trường hợp biên, không sửa tệp); `implementer` (thực hiện thay đổi và kiểm chứng); `reviewer` (rà soát độc lập, không sửa tệp).
- `subagent_calls` ở từng tác vụ và nhận xét: Chưa có dữ liệu chạy.
- Thông tin thiếu hoặc thừa khi giao việc (nếu có giao việc): Chưa có dữ liệu chạy.
- Ảnh hưởng đến token và thời gian: Chưa có dữ liệu chạy.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator, số skill bị xóa và lý do: Curator chạy 1 lần; sinh 3 skill; không xóa skill nào vì cả ba đều hợp lệ, tổng quát và không chứa định danh tác vụ evaluation.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `read-specifications-first` | Tổng quát: yêu cầu đọc đặc tả, liệt kê ràng buộc/tệp đầu ra trước khi thao tác; không lặp tên tác vụ hay dữ liệu học. | Đúng và phù hợp lỗi `tests_not_modified`; nhắc rõ ràng giới hạn sửa tệp. | 10 dòng. Description bắt đầu “Use when starting a new task”, phạm vi đủ rộng. Lần 3.4 ghi `skills_read=0` vì exception làm runner mất danh sách message chính. |
| `validate-against-rules` | Tổng quát: kiểm tra mọi quy tắc, tệp bị cấm, tệp đầu ra và định dạng, không chỉ test hiển thị. | Đúng và trực tiếp phòng ngừa các rule Acme về type hints, cents và CSV. | 11 dòng. Description kích hoạt sau khi thay đổi. Không suy luận rằng skill không được model dùng chỉ từ `skills_read=0` của lần exception. |
| `output-checklist` | Tổng quát: checklist xác minh tệp đầu ra, nội dung, định dạng và thay đổi bị cấm. | Đúng; có thể giúp trường hợp logs-learn không tạo `errors.json`. | 11 dòng. Description nêu tình huống kiểm tra output. Lần 3.4 đạt 1/9 nhưng chạm giới hạn đệ quy, nên chưa đủ bằng chứng về hiệu quả. |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

Chưa có dữ liệu hoàn chỉnh; sẽ chèn nguyên văn `report/table.md` và đầu ra `python scripts/check_breakdown.py` sau khi hoàn thành quy trình đóng băng. Lần `baseline/code-learn` bằng Gemini ngày 2026-10-06 bị lỗi hạ tầng `GoogleRateLimitError` (429 quota) và đã được chạy lại bằng OpenRouter. Lần `skills-auto/logs-learn` bằng OpenRouter đạt 1/9 rồi báo `GraphRecursionError` ở recursion limit 60, với `skills_read=0`, `tool_calls=0`, và 333,576 tokens; theo `03_runner.md`, đây là hệ quả của thiết kế runner khi `agent.invoke` ném exception, không chứng minh skill chưa được đọc.

## 8. Phân tích

Chưa có đủ dữ liệu thực nghiệm để so sánh ba điều kiện. Ba baseline learning bằng OpenRouter lần lượt đạt 6/10 (code), 5/8 (data), 0/9 (logs); không thể coi đây là so sánh điều kiện vì thiếu subagents và evaluation. Lần skills-auto duy nhất đạt 1/9 nhưng lỗi `GraphRecursionError`; theo GUIDE, lỗi runtime không dùng làm bằng chứng về hiệu quả skill. Lần Gemini bị `429 RESOURCE_EXHAUSTED` cũng là lỗi hạ tầng và không dùng để suy luận hiệu quả hay chi phí.

## 9. Hạn chế và tính hợp lệ

1. Quota Gemini free tier hết sau một lần chạy không hoàn chỉnh, nên chưa có đủ 6 tác vụ cho bất kỳ điều kiện nào. Vì vậy không thể ước lượng điểm trung bình, chi phí token hoặc chênh lệch giữa các điều kiện; mọi kết luận về hiệu quả đều chưa có giá trị.
2. Thiết kế gốc chỉ dự kiến một lần chạy cho mỗi cấu hình. Dù đủ quota, tính ngẫu nhiên của mô hình khiến chênh lệch nhỏ có thể là nhiễu thay vì tác động của subagent hoặc skill.
3. Bộ tác vụ do giảng viên thiết kế với các quy ước Acme cố định và chỉ dùng một mô hình Gemini. Kết quả, nếu có, chỉ khái quát hạn chế cho các họ code/data/logs và cấu hình model này; không suy rộng cho mọi bài toán tác tử.

## 10. Kết luận

Harness đã vượt toàn bộ kiểm tra ngoại tuyến trong Docker Linux. Tuy nhiên, quota Gemini cạn trước khi thu thập đủ kết quả nên chưa thể kết luận về hiệu quả của đa tác tử hoặc skill tự sinh. Bước tiếp theo là chạy lại toàn bộ ma trận thí nghiệm bằng một project có quota hợp lệ, giữ nguyên harness và quy trình đóng băng.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
  1. `python -m pytest tests/test_01_provided.py -q` (Windows, sau khi cài editable; đạt 15 passed với `--basetemp` cục bộ).
  2. `python scripts/tour.py`.
  3. `docker build -t lab-deepagents-local .`.
  4. `docker run --rm -v "$PWD:/lab" -w /lab lab-deepagents-local python -m pytest tests --basetemp /tmp/lab-pytest` (32 passed).
  5. `docker run --rm --env-file .env -v "$PWD:/lab" -w /lab lab-deepagents-local python -c "from lab.model import make_model; print(make_model().invoke('Reply with exactly OK').content)"` (Gemini trả `OK`).
  6. `python -m lab.runner --condition baseline --tasks learn` trong Docker với Gemini; dừng sau khi API trả `429 RESOURCE_EXHAUSTED` để tránh tạo thêm kết quả lỗi quota.
  7. Cấu hình OpenRouter free trong `.env`; chạy lần lượt `baseline` cho `code-learn` (6/10), `data-learn` (5/8), `logs-learn` (0/9); chạy `python -m lab.curator` (3 skill); chạy `skills-auto` cho `logs-learn` (1/9, `GraphRecursionError`).
- Thử thách mở rộng (nếu có): Chưa chọn.
- Ghi chú khác: Khóa Gemini chỉ được lưu cục bộ trong `.env` dưới biến `GOOGLE_API_KEY`; không đưa khóa vào mã nguồn, vết chạy hoặc báo cáo.
