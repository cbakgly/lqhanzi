#coding=utf-8
fuluzi = ["A00004-007", "A00004-008", "A00009-008-1", "A00010-024", "A00015-014", "A00015-016", "A00015-017", "A00015-018", "A00020-013", "A00020-014", "A00029-019", "A00029-020", "A00029-021", "A00037-039", "A00037-040", "A00044-038", "A00044-039", "A00044-040", "A00044-042", "A00045-073", "A00045-074", "A00045-076", "A00045-077", "A00045-078", "A00045-079", "A00045-080", "A00045-081", "A00048-022", "A00052-002", "A00061-014", "A00074-008", "A00086-032", "A00086-033", "A00091-013", "A00103-014", "A00103-015", "A00126-019", "A00137-005", "A00137-006", "A00144-005", "A00179-011", "A00241-024", "A00259-004", "A00264-005", "A00272-008", "A00273-020", "A00274-023", "A00274-024", "A00277-021", "A00279-029", "A00279-030", "A00279-031", "A00280-008", "A00283-014", "A00289-009", "A00290-019", "A00297-030", "A00297-034", "A00304-031", "A00309-011", "A00309-012", "A00317-018", "A00318-025", "A00335-017", "A00335-018", "A00335-019", "A00335-020", "A00335-021", "A00343-004", "A00344-018", "A00346-006", "A00346-007", "A00352-011", "A00355-022", "A00355-023", "A00358-012", "A00358-013", "A00360-014", "A00360-015", "A00362-024", "A00364-010", "A00364-011", "A00375-003", "A00404-021", "A00410-011", "A00418-006", "A00419-012", "A00419-013", "A00424-013", "A00432-010", "A00449-010", "A00454-017", "A00455-005", "A00460-029", "A00463-041", "A00466-013", "A00466-014", "A00466-015", "A00466-016", "A00467-037", "A00486-004", "A00514-021", "A00518-006", "A00526-016", "A00526-017", "A00526-018", "A00526-019", "A00526-020", "A00531-006", "A00537-002", "A00540-015", "A00556-005", "A00558-007", "A00558-008", "A00561-020", "A00568-008", "A00568-009", "A00593-022", "A00593-023", "A00596-007", "A00597-003", "A00602-001", "A00609-009", "A00611-002", "A00611-003", "A00628-033", "A00628-034", "A00628-035", "A00628-036", "A00658-012", "A00660-018", "A00664-011", "A00667-019", "A00667-020", "A00668-018", "A00684-010", "A00691-003", "A00702-001", "A00707-025", "A00712-003", "A00712-004", "A00714-070", "A00718-021", "A00718-022", "A00725-003", "A00726-013", "A00734-033", "A00734-037", "A00734-039", "A00736-023", "A00739-063", "A00750-009", "A00763-017", "A00776-010", "A00779-001", "A00781-018", "A00781-019", "A00786-029", "A00793-013", "A00802-018", "A00803-011", "A00816-016", "A00816-018", "A00816-021", "A00822-011", "A00823-090", "A00823-091", "A00826-021", "A00829-021", "A00835-042", "A00843-025", "A00843-026", "A00843-027", "A00843-028", "A00846-035", "A00849-027-3", "A00849-028", "A00849-029", "A00849-030", "A00849-032", "A00849-035", "A00849-036", "A00851-007", "A00865-031", "A00875-023", "A00876-023", "A00878-004", "A00883-010", "A00883-011", "A00883-012", "A00883-013", "A00888-005", "A00888-006", "A00889-003", "A00892-005", "A00895-003", "A00908-010", "A00931-001", "A00939-024", "A00939-025", "A00951-017", "A00977-014", "A00979-005", "A00986-033", "A00986-034", "A00986-035", "A00994-008", "A01013-004", "A01016-019", "A01016-020", "A01025-013", "A01033-034", "A01033-036", "A01038-016", "A01041-025", "A01043-030", "A01046-018", "A01048-052", "A01048-053", "A01056-044", "A01059-034", "A01059-035", "A01059-036", "A01060-012", "A01064-022", "A01065-038", "A01073-009", "A01075-013", "A01076-002", "A01079-024", "A01081-014", "A01081-016", "A01082-018", "A01082-019", "A01082-020", "A01086-016", "A01086-017", "A01090-010", "A01097-039", "A01099-003", "A01102-017", "A01107-047", "A01127-004", "A01129-017", "A01135-004", "A01139-011", "A01147-015", "A01152-014", "A01152-015", "A01159-018", "A01164-015", "A01164-016", "A01164-017", "A01169-002", "A01171-015", "A01171-016", "A01171-017", "A01181-013", "A01192-014", "A01192-015", "A01196-023", "A01196-024", "A01204-024", "A01207-010", "A01207-012", "A01211-003", "A01214-017", "A01239-011", "A01240-021", "A01243-008", "A01244-015", "A01244-016", "A01255-008", "A01255-009-1", "A01275-008", "A01288-036", "A01288-037", "A01288-038", "A01295-057", "A01295-058-1", "A01295-059-1", "A01295-060", "A01296-047", "A01310-011", "A01330-024", "A01330-025", "A01332-005", "A01334-030", "A01362-010", "A01363-017", "A01382-025", "A01382-027", "A01382-028", "A01385-025", "A01389-006", "A01390-019", "A01390-020", "A01392-005", "A01392-006", "A01404-044", "A01404-046", "A01409-011", "A01422-004", "A01423-016", "A01426-008", "A01448-002", "A01457-029", "A01458-008", "A01464-067", "A01464-068", "A01464-069", "A01473-027", "A01495-007", "A01511-007", "A01511-008", "A01518-017", "A01518-018", "A01518-019", "A01535-010", "A01535-011", "A01548-005", "A01564-017", "A01568-004", "A01571-005", "A01573-003", "A01578-005", "A01578-006", "A01591-005", "A01592-035", "A01592-036", "A01592-038", "A01592-039", "A01594-004", "A01594-006", "A01605-003", "A01623-008", "A01623-009", "A01630-006", "A01630-007", "A01632-018", "A01643-023", "A01643-024", "A01643-025", "A01650-005", "A01650-007", "A01663-002", "A01679-032", "A01679-034", "A01682-004", "A01690-026", "A01695-017", "A01695-018", "A01703-037", "A01705-018", "A01705-019", "A01705-020", "A01715-005-1", "A01720-011", "A01725-008", "A01725-009", "A01727-020", "A01727-021", "A01728-027", "A01733-027", "A01733-028", "A01734-051", "A01734-052", "A01734-053", "A01735-019", "A01735-021", "A01735-022-1", "A01747-011", "A01750-014", "A01752-014", "A01756-011", "A01758-034", "A01758-038", "A01758-039", "A01761-029", "A01761-030", "A01762-019", "A01762-020", "A01765-034", "A01768-009", "A01770-032", "A01771-008", "A01779-018", "A01781-007", "A01784-017", "A01787-017", "A01787-018", "A01796-007", "A01797-007", "A01797-008", "A01816-011", "A01826-009", "A01827-008", "A01828-008", "A01831-017", "A01834-012", "A01840-025", "A01840-026", "A01840-027", "A01840-028", "A01840-030", "A01840-031", "A01840-032", "A01840-033", "A01840-034", "A01840-035", "A01840-036", "A01840-037", "A01848-058", "A01851-002", "A01862-014", "A01913-002", "A01932-017", "A01944-036", "A01950-011", "A01955-018", "A01956-023", "A01979-031", "A01981-010-1", "A01995-006", "A02006-001", "A02024-019", "A02056-019", "A02056-021", "A02056-022", "A02073-053", "A02073-055", "A02073-056", "A02073-057", "A02073-058", "A02073-059", "A02073-060", "A02073-061", "A02073-062", "A02073-063", "A02073-064", "A02075-079", "A02075-080", "A02075-081-1", "A02079-007", "A02079-008", "A02088-010", "A02088-011", "A02091-088", "A02091-089", "A02091-090", "A02091-091", "A02093-026-1", "A02094-021", "A02095-028", "A02102-008", "A02105-005", "A02115-044", "A02124-008", "A02134-005", "A02161-027", "A02170-008", "A02183-019", "A02183-020", "A02183-021", "A02183-022", "A02183-023", "A02184-012-1", "A02189-011", "A02207-002", "A02210-006", "A02214-029", "A02235-005", "A02243-022", "A02255-005", "A02273-004", "A02274-010", "A02306-008", "A02307-013", "A02307-014", "A02309-038", "A02311-026", "A02337-002", "A02341-008", "A02346-020", "A02346-021", "A02354-042", "A02354-043", "A02374-006", "A02378-012", "A02384-005", "A02388-007", "A02391-044", "A02391-045", "A02395-018", "A02407-017", "A02409-028", "A02411-015", "A02415-017", "A02415-018", "A02416-063", "A02416-064", "A02416-065", "A02424-035", "A02424-036", "A02424-039", "A02424-040", "A02424-041", "A02424-042", "A02424-043", "A02424-044", "A02429-036", "A02430-005", "A02430-006", "A02430-007", "A02430-008", "A02430-009", "A02430-010", "A02432-028", "A02432-029", "A02432-032", "A02453-027", "A02455-005", "A02456-005", "A02468-012", "A02470-068", "A02477-022", "A02477-023", "A02477-024", "A02487-004", "A02496-008", "A02501-021", "A02504-011", "A02504-012", "A02510-020", "A02512-002", "A02525-017", "A02538-002", "A02539-015", "A02541-017", "A02552-014", "A02552-016", "A02565-005", "A02575-003", "A02580-006", "A02591-013", "A02594-031", "A02604-010", "A02611-012", "A02611-013", "A02613-001-1", "A02615-009", "A02615-010", "A02618-006", "A02622-010", "A02622-011", "A02628-001", "A02642-029", "A02643-008", "A02654-038", "A02654-039", "A02654-040", "A02656-018", "A02659-037", "A02701-044", "A02701-045", "A02703-002", "A02710-003", "A02714-003", "A02719-019", "A02720-055", "A02723-003", "A02726-020", "A02726-023", "A02728-010", "A02730-004", "A02730-005", "A02732-018", "A02732-019", "A02734-009", "A02735-030", "A02735-032", "A02738-017", "A02744-002", "A02750-009", "A02752-021", "A02763-014", "A02764-011", "A02772-042", "A02772-043", "A02779-032", "A02779-033", "A02779-034", "A02792-008", "A02792-009", "A02795-001", "A02798-007", "A02806-002", "A02807-008", "A02816-019", "A02816-020", "A02817-015", "A02817-016", "A02835-014", "A02844-017", "A02844-018", "A02861-002", "A02862-017", "A02862-018", "A02864-006", "A02865-017", "A02871-003", "A02873-020", "A02873-021", "A02878-024", "A02878-026", "A02888-014", "A02890-030", "A02891-005", "A02901-032", "A02902-038", "A02903-026", "A02906-033", "A02907-040", "A02908-011", "A02908-012", "A02908-013", "A02918-052", "A02920-005", "A02936-010", "A02936-011", "A02940-031", "A02940-033", "A02940-034", "A02947-006", "A02950-019", "A02956-006", "A02957-006", "A02958-020", "A02958-021", "A02958-022", "A02958-023-1", "A02960-021", "A02965-008", "A02966-011", "A02966-012", "A02971-021", "A02974-012", "A02975-006", "A02976-045", "A02997-015", "A02998-027", "A02998-028", "A02998-029", "A02998-030", "A02998-031", "A03007-036", "A03009-011", "A03010-030", "A03013-025", "A03017-012", "A03026-028", "A03045-006", "A03045-007", "A03060-010", "A03061-003", "A03061-004", "A03061-005", "A03069-004", "A03073-035", "A03073-037", "A03073-038", "A03080-011", "A03081-013", "A03089-008", "A03092-014", "A03092-015", "A03096-004", "A03102-004", "A03112-012", "A03113-042", "A03113-043", "A03117-026", "A03117-027", "A03121-006", "A03126-002", "A03135-007", "A03137-015", "A03138-027", "A03146-022", "A03150-007", "A03152-009", "A03158-007", "A03164-033", "A03165-009", "A03165-010", "A03165-011", "A03168-006", "A03172-057", "A03184-022", "A03188-023", "A03188-024", "A03195-010", "A03199-008", "A03200-011", "A03203-035", "A03203-038", "A03205-035", "A03205-036", "A03205-037", "A03209-013", "A03214-039-1", "A03214-040", "A03218-033", "A03218-034", "A03220-009", "A03221-016", "A03221-017", "A03222-026", "A03223-045", "A03223-046", "A03223-047", "A03226-007", "A03228-022", "A03229-028", "A03230-017", "A03231-003", "A03232-014", "A03233-014", "A03241-006", "A03245-014", "A03246-018", "A03250-006", "A03250-007", "A03250-008", "A03251-018", "A03252-009", "A03255-007", "A03255-008", "A03255-009", "A03256-007", "A03263-010", "A03270-084", "A03270-085", "A03270-086", "A03270-087", "A03270-089", "A03270-091", "A03270-092", "A03270-095", "A03270-096", "A03272-021", "A03272-022", "A03273-029", "A03273-030", "A03273-031", "A03274-003", "A03282-021", "A03285-022", "A03285-023", "A03286-055", "A03286-056", "A03286-057", "A03289-004", "A03294-004", "A03304-008", "A03305-017", "A03305-018", "A03307-020", "A03317-006", "A03317-007", "A03326-032", "A03328-009", "A03328-010", "A03346-003", "A03347-011", "A03348-002", "A03350-007", "A03352-010", "A03354-029", "A03362-018", "A03362-019", "A03364-021", "A03364-022", "A03365-009", "A03367-002", "A03372-011", "A03372-012-1", "A03377-027", "A03382-006", "A03387-013", "A03387-014", "A03387-015", "A03387-016", "A03389-011", "A03390-024", "A03390-025", "A03391-069", "A03400-047", "A03400-048", "A03400-050", "A03400-051", "A03400-052", "A03400-054-1", "A03419-013", "A03426-029", "A03426-030", "A03426-031", "A03427-022", "A03427-023", "A03427-024", "A03442-018", "A03450-041", "A03467-002", "A03467-003", "A03469-018", "A03469-020", "A03472-001", "A03473-021", "A03486-024", "A03493-005", "A03497-001", "A03503-100", "A03512-007", "A03526-058", "A03526-059", "A03527-012", "A03528-008", "A03532-018", "A03542-007", "A03542-008", "A03568-029", "A03586-056", "A03603-003", "A03604-038-1", "A03605-030", "A03605-032", "A03606-032", "A03606-033", "A03610-006", "A03612-063", "A03615-004", "A03615-005", "A03622-010", "A03634-031", "A03634-032", "A03634-033", "A03640-007", "A03642-004", "A03649-011", "A03671-005", "A03688-002", "A03701-007", "A03701-008", "A03701-009", "A03704-026", "A03706-037", "A03706-038", "A03706-039", "A03706-040", "A03706-041", "A03706-042", "A03706-043", "A03706-044", "A03706-045", "A03709-035", "A03709-036", "A03709-037", "A03709-038", "A03709-039", "A03709-040", "A03709-041", "A03709-042", "A03709-043", "A03711-003", "A03712-027", "A03712-028", "A03714-007", "A03714-008", "A03715-003-1", "A03715-004", "A03718-006", "A03727-038", "A03727-039", "A03733-002", "A03744-008", "A03745-033", "A03750-011", "A03751-012", "A03760-032", "A03762-027", "A03762-028", "A03762-029", "A03762-030", "A03762-031", "A03762-032", "A03763-020", "A03763-021", "A03764-014", "A03765-015", "A03768-027", "A03769-013", "A03770-024", "A03775-022", "A03780-012", "A03780-013", "A03781-010", "A03781-011", "A03781-012", "A03781-013", "A03811-014", "A03811-015", "A03811-017", "A03817-005", "A03818-008", "A03829-005", "A03836-011", "A03837-017", "A03837-018", "A03839-007", "A03842-012", "A03842-013", "A03843-005", "A03844-006", "A03844-007", "A03848-016", "A03850-014", "A03853-011", "A03869-003", "A03877-007", "A03877-008", "A03883-009", "A03885-031", "A03885-032", "A03885-033", "A03907-007", "A03914-024", "A03916-025", "A03916-026", "A03917-013", "A03917-016", "A03920-014", "A03923-019", "A03925-044", "A03928-011", "A03928-012", "A03934-010", "A03937-008", "A03938-005", "A03938-006", "A03954-002", "A03971-013", "A03974-009", "A03977-013", "A03978-009", "A03979-010", "A03979-011-1", "A03979-012", "A03984-006", "A03984-007-1", "A03986-009", "A03989-019", "A03989-020", "A03989-021", "A03992-024", "A03992-025-1", "A03992-026", "A03992-027", "A04000-041", "A04010-005", "A04012-031", "A04012-032", "A04033-005", "A04034-007", "A04039-001", "A04056-018", "A04058-009", "A04073-047", "A04073-049", "A04073-050", "A04073-052", "A04073-053", "A04076-013", "A04081-002", "A04082-008", "A04084-008", "A04086-007", "A04086-008", "A04087-004", "A04095-013", "A04095-014", "A04097-005", "A04100-035", "A04100-036", "A04103-034", "A04107-069", "A04107-070", "A04107-071", "A04108-028", "A04108-029", "A04109-023", "A04109-024", "A04109-025", "A04114-009", "A04117-014", "A04119-013", "A04120-005", "A04124-010", "A04128-006", "A04130-030", "A04134-005", "A04137-009", "A04151-010", "A04151-011", "A04151-012", "A04152-012", "A04152-013", "A04158-015", "A04158-016", "A04158-017", "A04158-018", "A04160-012", "A04161-011", "A04163-007", "A04165-004", "A04165-007", "A04171-017", "A04171-018", "A04173-028", "A04173-029", "A04173-031", "A04176-042", "A04176-043", "A04176-044", "A04176-046", "A04177-026", "A04177-027", "A04177-028", "A04178-014", "A04182-088", "A04182-089", "A04182-090", "A04182-091", "A04183-015", "A04184-006", "A04192-009", "A04196-064", "A04196-065", "A04196-066", "A04196-067", "A04196-068", "A04196-069", "A04196-070", "A04196-071", "A04196-072", "A04196-073", "A04196-074", "A04197-007", "A04200-003", "A04203-033", "A04203-034", "A04203-035", "A04203-036", "A04203-038", "A04204-025", "A04207-008", "A04209-005", "A04214-023", "A04215-014", "A04220-037", "A04230-003", "A04231-010", "A04238-025", "A04238-026", "A04261-035", "A04261-036", "A04261-037", "A04264-005", "A04269-003", "A04278-004", "A04312-004", "A04322-004", "A04322-005", "A04336-005", "A04346-008", "A04368-086", "A04368-087", "A04368-088", "A04368-089", "A04368-090", "A04368-092", "A04369-028", "A04372-003", "A04373-020", "A04375-014", "A04375-015", "A04376-020", "A04376-021", "A04376-022", "A04377-008", "A04378-010", "A04389-020", "A04390-011", "A04396-003", "A04397-009", "A04405-008", "A04406-008", "A04410 正", "A04411-007", "A04422-018", "A04424-029", "A04425-042", "A04425-043", "A04425-044", "A04425-046", "A04425-048", "A04425-049", "A04432-019", "A04434-039", "A04434-040", "A04437-014", "A04437-015", "A04437-016", "A04437-017", "A04447-010", "A04448-047-1", "A04448-048", "A04450-008", "A04458-011", "A04462-013", "A04462-014", "A04463-026", "A04463-027", "A04464-017", "A04467-059", "A04467-061", "A04475-017", "A04490-015", "A04491-033", "A04496-006", "A04497-145", "A04497-146", "A04497-147", "A04497-148", "A04503-010", "A04504-004", "A04506-008", "A04507-018", "A04518-019", "A04525-017", "A04528-026", "A04531-004", "A04533-009", "A04535-033", "A04535-034", "A04539-003", "A04540-012", "A04541-010", "A04541-011", "A04541-012", "A04544-016", "A04544-017", "A04544-018", "A04554-019", "A04555-009-1", "A04566-038", "A04566-039", "A04566-041", "A04570-007", "A04572-042", "A04572-043", "A04578-025", "A04581-015", "A04581-016", "A04600-006", "A04600-007", "A04600-008", "A04605-008", "A04615-014", "A04615-015", "A04615-016", "A04616-018", "A04616-019", "A04643-022", "A04652-014", "A04656-009", "A04658-005", "A04659-001", "A04664-007", "A04665-019", "A04665-020", "A04665-022", "A04666-017", "A04666-018", "A04667-012", "A04668-014", "A04673-005", "A04678-029", "A04678-030", "A04678-031", "A04681-053", "A04681-054", "A04681-055", "A04681-056", "A04683-028", "A04684-022", "A04684-023", "A04684-024", "A04684-025", "A04686-075", "A04686-076", "A04686-078", "A04686-079", "A04687-010", "A04693-017", "A04693-018", "A04693-019", "A04693-020", "A04704-003", "A04706-012", "A04706-013", "A04708-002", "A04712-015", "A04712-016", "A04719-011", "A04720-035", "A04720-036", "A04720-037", "A04720-038", "A04737-012", "A04737-013", "A04740-018", "A04741-011", "A04741-012", "A04751-025", "A04754-009", "A04756-033", "A04765-019", "A04767-014", "A04769-028", "A04773-016", "A04783-005", "A04785-064", "A04785-065", "A04785-066", "A04785-067", "A04786-034", "A04786-035", "A04786-036", "A04786-037", "A04786-040", "A04786-041", "A04786-042", "A04793-007", "A04794-056", "A04794-057", "A04794-058", "A04796-056", "A04796-057", "A04796-058", "A04796-059", "A04796-060", "A04796-061", "A04796-062", "A04796-063", "A04796-064", "A04805-005", "A04805-006", "A04806-054", "A04806-055", "A04806-056", "A04807-012", "A04808-127", "A04808-128", "A04808-129", "A04808-130", "A04808-131", "A04808-132", "A04808-133", "A04808-136", "A04808-137", "B00015-006", "B00015-007", "B00016-016", "B00016-017", "B00109-002", "B00134-010", "B00145-023", "B00145-024", "B00145-025", "B00171-004", "B00185-010", "B00200-003", "B00204-009", "B00204-010", "B00204-011", "B00220-001", "B00227-003", "B00237-013", "B00237-014", "B00237-015", "B00239-001", "B00248-006", "B00288-025", "B00293-001", "B00315-003", "B00330-005", "B00350-002", "B00356-002", "B00364-005", "B00369-004", "B00376-005", "B00394-010", "B00394-011", "B00449-001", "B00458-003", "B00459-019", "B00468-005", "B00493-002", "B00509-009", "B00509-010", "B00513-020", "B00513-021", "B00524-009", "B00524-010", "B00524-011", "B00524-012", "B00525-019", "B00542-009", "B00542-010", "B00544-001", "B00561-001", "B00566-005", "B00566-006", "B00647-002", "B00697-003", "B00713-006", "B00732-001", "B00764-023", "B00764-024", "B00764-025", "B00775-017", "B00776-005", "B00781-003", "B00783-002", "B00796-001", "B00799-002", "B00805-007", "B00813-002", "B00819-002", "B00820-013", "B00820-014", "B00837-006", "B00837-007", "B00845-013", "B00904-005", "B00908-016", "B00908-017", "B00933-008", "B00946-007", "B00963-002", "B00977-005", "B00988-014", "B00988-015", "B00989-028", "B01022-013", "B01022-014", "B01022-015", "B01047-002", "B01063-002", "B01067-003", "B01071-002", "B01117-011", "B01117-012", "B01117-013", "B01145-005", "B01145-006", "B01149-013", "B01149-014", "B01149-015", "B01149-016", "B01163-002", "B01193-002", "B01201-004", "B01212-003", "B01228-004", "B01286-001", "B01292-009", "B01326-001", "B01366-001", "B01371-006", "B01371-007", "B01371-008", "B01378-005", "B01384-010", "B01384-011", "B01395-009", "B01401-002", "B01404-005", "B01415-003", "B01420-002", "B01452-003", "B01457-003", "B01471-016", "B01485-007", "B01485-008", "B01487-004", "B01487-005", "B01490-003", "B01500-019", "B01505-015", "B01506-005", "B01516-005", "B01532-003", "B01541-001", "B01541-002", "B01571-005", "B01577-002", "B01582-014", "B01583-001", "B01609-005", "B01624-003", "B01629-007", "B01636-005", "B01655-006", "B01689-009", "B01718-002", "B01719-001", "B01760-005", "B01764-001", "B01764-002", "B01805-002", "B01810-008", "B01853-004", "B01854-011", "B01854-012", "B01854-013", "B01857-004", "B01867-014", "B01867-015", "B01898-006", "B01918-007", "B01922-006", "B01929-002", "B01938-006", "B01938-007", "B01959-009", "B01968-005", "B01970-002", "B01986-004", "B01989-007", "B01989-008", "B01990-001", "B01991-008", "B01993-017", "B01993-018", "B01996-016", "B01996-017", "B01996-018", "B01997-014", "B01998-001", "B02028-002", "B02046-003", "B02065-001", "B02079-002", "B02094-001", "B02101-001", "B02110-002", "B02119-004", "B02127-006", "B02138-005", "B02179-002", "B02218-003", "B02226-014", "B02226-015", "B02226-016", "B02261-006", "B02272-008", "B02281-006", "B02281-007", "B02297-008", "B02297-009", "B02314-002", "B02342-005", "B02345-008", "B02350-005", "B02350-006", "B02351-003", "B02404-003", "B02433-008", "B02440-007", "B02442-007", "B02492-004", "B02495-003", "B02497-010", "B02497-011", "B02512-013", "B02512-014", "B02543-009", "B02548-005", "B02549-003", "B02562-006", "B02562-007", "B02591-004", "B02625-002", "B02626-001", "B02628-004", "B02628-005", "B02630-003", "B02631-005", "B02634-008", "B02640-002", "B02648-003", "B02649-012", "B02649-013", "B02649-014", "B02665-006", "B02680-005", "B02694-005", "B02694-006", "B02694-007", "B02694-008", "B02696-001-1", "B02701-002", "B02707-014", "B02720-005", "B02737-003", "B02737-004", "B02758-001", "B02761-001", "B02775-001", "B02792-005", "B02795-004", "B02795-005", "B02795-006", "B02800-008", "B02815-006", "B02817-004", "B02828-002", "B02844-011", "B02851-004", "B02854-002", "B02855-001", "B02855-002", "B02855-003", "B02897-004", "B02903-004", "B02903-005", "B02904-007", "B02942-003", "B02949-006", "B02949-007", "B02950-001", "B02959-002", "B02990-001", "B02999-005", "B02999-006", "B03003-012", "B03003-013", "B03003-014", "B03005-004", "B03009-002", "B03012-006", "B03012-007", "B03013-003", "B03030-003", "B03039-009", "B03048-002", "B03059-007", "B03072-005", "B03080-004", "B03083-003", "B03086-004", "B03135-001", "B03159-005", "B03161-001", "B03167-006", "B03167-007", "B03170-002", "B03214-006", "B03229-010", "B03233-002", "B03241-001", "B03245-003", "B03254-001", "B03258-014", "B03258-015", "B03259-004", "B03271-004", "B03299-004", "B03309-009", "B03380-007", "B03384-001", "B03397-008-1", "B03403-007", "B03407-006", "B03407-007", "B03425-006", "B03425-007", "B03455-003", "B03479-005", "B03484-001", "B03491-007", "B03494-003", "B03502-010", "B03502-011", "B03505-025", "B03505-026", "B03507-005", "B03514-013", "B03514-014", "B03528-016", "B03530-011", "B03530-012", "B03531-009", "B03531-010", "B03533-009", "B03567-003", "B03574-004", "B03581-003", "B03584-017", "B03584-018", "B03596-001", "B03601-005", "B03618-008", "B03621-001", "B03627-004", "B03640-013", "B03650-005", "B03654-004", "B03675-008", "B03688-002", "B03694-004", "B03703-002", "B03719-006", "B03730-004", "B03735-010", "B03743-002", "B03743-003", "B03758-001", "B03794-005", "B03805-003", "B03843-005", "B03889-013", "B03889-014", "B03909-002", "B03919-005", "B03928-009", "B03928-010", "B03944-011", "B03973-001", "B04007-001", "B04019-001", "B04110-004", "B04118-013", "B04121-002", "B04155-006", "B04167-002", "B04200-003", "B04200-004-1", "B04202-001", "B04203-004", "B04205-009", "B04215-011", "B04215-013", "B04219-007", "B04235-002", "B04251-006", "B04252-004", "B04273-002", "B04279-003", "B04302-005", "B04325-006", "B04359-003", "B04366-003", "B04412-003", "B04422-002", "B04442-004", "B04456-005", "B04459-005", "B04465-002", "B04465-003", "B04465-004", "B04477-005", "B04488-004", "B04494-001", "B04501-001", "B04517-002", "B04518-002", "B04524-003", "B04554-001", "B04571-002", "B04573-002", "B04583-006", "B04583-007", "B04586-003", "B04587-007", "B04620-003", "B04622-009", "B04624-004", "B04631-013", "B04652-001", "B04654-003", "B04654-004", "B04661-003", "B04668-001", "B04669-004", "B04707-008", "B04711-002", "B04714-015", "B04716-002", "B04761-008", "B04770-001", "B04773-003", "B04804-006", "B04804-007", "B04837-003", "B04887-005", "B04899-002", "B04902-008", "B04903-016", "B04914-003", "B04957-003", "B04957-004", "B04958-003", "B04962-002", "B05029-003", "B05037-004", "B05092-001", "B05092-002", "B05095-002", "B05099-002", "B05129-001", "B05131-003", "B05146-003", "B05146-004", "B05160-002", "B05182-001", "B05185-006", "B05190-003", "B05203-005", "B05204-005", "B05234-004", "B05234-005", "B05239-007", "B05242-005", "B05251-018", "B05267-010", "B05279-002", "B05281-002", "B05281-003", "B05287-014", "B05299-001", "B05327-005", "B05328-003", "B05331-001", "B05333-003", "B05351-002", "B05359-003", "B05367-008", "B05385-002", "B05400-005", "B05430-007", "B05440-008", "B05442-002", "B05445-001", "B05445-002", "B05508-023", "B05510-003", "B05518-005", "B05541-011", "B05542-003", "B05553-006", "B05557-010", "B05593-005-1", "B05616-013", "B05628-001", "B05667-004", "B05683-007", "B05683-008", "B05700-002", "B05704-006", "B05708-005", "B05709-004", "B05709-005", "B05725-007", "B05741-002", "B05802-005", "B05836-010", "B05875-003", "B05887-005", "B05912-007", "B05920-010", "B05923-013", "B05958-007", "B05975-007", "B05996-006", "B06057-002", "B06090-007", "B06106-014", "B06119-001", "B06149-011", "B06150-007", "B06176-009", "B06188-015", "B06198-005", "B06199-004", "B06204-008", "B06245-011", "B06247-008", "B06249-006", "B06252-008", "B06253-005", "B06256-006", "B06259-013", "B06260-010", "B06260-011", "B06262-019", "B06263-006", "B06266-011", "B06266-012", "B06301-003-1", "B06303-015", "B06303-016", "B06303-017", "B06303-018", "B06304-037", "B06309-004", "B06309-005", "B06316-020", "C00225-005", "C00282-005", "C00370-005", "C00375-006", "C00387-002", "C00420-002", "C00488-004", "C00504-003", "C00530-001", "C00579-001", "C00627-005-1", "C00672-002", "C00763-002", "C01148-002", "C01154-001", "C01380-001", "C01472-007", "C01520-005", "C01560-002", "C01692-002", "C01747-001", "C01875-002", "C01939-002", "C01939-003", "C01948-005", "C01995-003", "C02085-003", "C02325-002", "C02459-002", "C02460-002", "C02461-006", "C02597-002", "C02601-006", "C02609-002", "C02611-002", "C02655-001", "C03003-001", "C03057-001", "C03130-003", "C03167-001", "C03209-001", "C03337-001", "C03383-002", "C03439-002", "C03473-010", "C03476-006", "C03476-007", "C03765-001", "C03817-002", "C03841-001", "C03857-001", "C03896-001", "C04041-006", "C04042-004", "C04162-004", "C04204-004", "C04524-001", "C04568-006", "C04572-001", "C04575-002", "C04599-002", "C04648-002", "C04693-001", "C04693-002", "C04772-008", "C04827-001", "C05016-001", "C05130-002", "C05356-001", "C05422-001", "C05448-001", "C05616-001", "C05688-001", "C05954-001", "C06001-002", "C06028-001", "C06122-001", "C06323-002", "C06346-001", "C06556-001", "C06585-001", "C06690-006", "C06867-006", "C06903-002", "C07403-001", "C07513-002", "C07648-001", "C08048-003", "C08073-007", "C08234-001", "C08234-002", "C08234-003", "C08801-002", "C08993-002", "C09459-001", "C09716-002", "C10430-006", "C10435-001", "C10488-003", "C10498-003", "C10555-001", "C10942-003", "C10990-005", "C11102-006", "C11117-005", "C11167-001", "C11170-001", "C11195-005", "C11385-001", "C11408-003", "C11709-001", "C12174-006", "C12273-003", "C12757-005", "C12777-002", "C12933-003", "C13010-003", "C13216-013", "C13599-001", "C13674-001", "C14448-004", "C14459-002", "C14679-001", "C14927-001", "C15224-002", "C15404-002", "C15623-004", "C15814-004", "C15840-001", "C15841-003", "C15841-004", "C15846-001", "C15853-001", "C15853-002", "C15867-001", "C15871-001", "C15878-001", "C15893-001", "C15903-001", "C15905-001", "C15905-002", "C15935-001", "C15941-001", "C15941-002", "C15952-001", "C15972-002", "C15978-001", "C16095-001", "C16902-003", "C16991-001", "C17042-005", "C17056-003", "C17082-001", "C17082-002", "C17082-003", "C17115-001", "C17143-003", "C18067-002", "C18139-002", "C18212-004", "C18213-004", "C18445-010", "C18445-011", "N00083-010", "N00098-009", "N00226-001", "N00239-001", "N00249-002", "N00351-005", "N00434-002", "N00434-003", "N00438-004"]