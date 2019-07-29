from peewee import *

database = MySQLDatabase("prod", host="db1-cluster.cluster-cy3jhnakv3ox.us-east-2.rds.amazonaws.com", port=3306, user="root", passwd="aoeusnth")

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class T30DayHistorySales(BaseModel):
    qty = IntegerField()
    sales_date = DateField()
    sku = CharField(index=True)

    class Meta:
        table_name = '30_day_history_sales'

class Dpsusers(BaseModel):
    badge_id = CharField(null=True)
    create_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    dept_id = IntegerField(null=True)
    email = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    office_hours = TextField(null=True)
    password = CharField(null=True)
    pin = CharField(null=True)
    security_level = IntegerField(null=True)
    shipworks_username = CharField(null=True)
    status = BooleanField(default=True)  # bit
    user_id = AutoField()
    username = CharField(null=True)

    class Meta:
        table_name = 'DPSUsers'

class DpsusersReceivingcount(BaseModel):
    count = IntegerField(null=True)
    timestamp = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    user_id = IntegerField(null=True)

    class Meta:
        table_name = 'DPSUsers_ReceivingCount'

class AdminAssert(BaseModel):
    assert_data = TextField(null=True)
    assert_id = AutoField()
    assert_type = CharField(null=True)

    class Meta:
        table_name = 'admin_assert'

class AdminRole(BaseModel):
    parent_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    role_id = AutoField()
    role_name = CharField(null=True)
    role_type = CharField(constraints=[SQL("DEFAULT '0'")])
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    tree_level = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    user_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'admin_role'
        indexes = (
            (('parent_id', 'sort_order'), False),
        )

class AdminRule(BaseModel):
    assert_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    permission = CharField(null=True)
    privileges = CharField(null=True)
    resource_id = CharField(null=True)
    role = ForeignKeyField(column_name='role_id', constraints=[SQL("DEFAULT 0")], field='role_id', model=AdminRole)
    role_type = CharField(null=True)
    rule_id = AutoField()

    class Meta:
        table_name = 'admin_rule'
        indexes = (
            (('resource_id', 'role'), False),
            (('role', 'resource_id'), False),
        )

class AdminUser(BaseModel):
    created = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    email = CharField(null=True)
    extra = TextField(null=True)
    firstname = CharField(null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")])
    lastname = CharField(null=True)
    logdate = DateTimeField(null=True)
    lognum = IntegerField(constraints=[SQL("DEFAULT 0")])
    modified = DateTimeField(null=True)
    password = CharField(null=True)
    reload_acl_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    rp_token = TextField(null=True)
    rp_token_created_at = DateTimeField(null=True)
    user_id = AutoField()
    username = CharField(null=True, unique=True)

    class Meta:
        table_name = 'admin_user'

class AdminnotificationInbox(BaseModel):
    date_added = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    description = TextField(null=True)
    is_read = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_remove = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    notification_id = AutoField()
    severity = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    title = CharField()
    url = CharField(null=True)

    class Meta:
        table_name = 'adminnotification_inbox'

class AmMenu(BaseModel):
    block_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    cms_page_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    image = CharField(null=True)
    menu_id = AutoField()
    modified = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField(constraints=[SQL("DEFAULT ''")])
    parent_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    position = IntegerField(constraints=[SQL("DEFAULT 0")])
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    url = CharField(null=True)

    class Meta:
        table_name = 'am_menu'

class AmMenuStore(BaseModel):
    menu_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'am_menu_store'
        indexes = (
            (('menu_id', 'store_id'), True),
        )
        primary_key = CompositeKey('menu_id', 'store_id')

class Api2AclAttribute(BaseModel):
    allowed_attributes = TextField(null=True)
    entity_id = AutoField()
    operation = CharField()
    resource_id = CharField()
    user_type = CharField(index=True)

    class Meta:
        table_name = 'api2_acl_attribute'
        indexes = (
            (('user_type', 'resource_id', 'operation'), True),
        )

class Api2AclRole(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], index=True)
    entity_id = AutoField()
    role_name = CharField()
    updated_at = DateTimeField(index=True, null=True)

    class Meta:
        table_name = 'api2_acl_role'

class Api2AclRule(BaseModel):
    entity_id = AutoField()
    privilege = CharField(null=True)
    resource_id = CharField()
    role = ForeignKeyField(column_name='role_id', field='entity_id', model=Api2AclRole)

    class Meta:
        table_name = 'api2_acl_rule'
        indexes = (
            (('role', 'resource_id', 'privilege'), True),
        )

class Api2AclUser(BaseModel):
    admin = ForeignKeyField(column_name='admin_id', field='user_id', model=AdminUser, unique=True)
    role = ForeignKeyField(column_name='role_id', field='entity_id', model=Api2AclRole)

    class Meta:
        table_name = 'api2_acl_user'
        primary_key = False

class ApiAssert(BaseModel):
    assert_data = TextField(null=True)
    assert_id = AutoField()
    assert_type = CharField(null=True)

    class Meta:
        table_name = 'api_assert'

class ApiRole(BaseModel):
    parent_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    role_id = AutoField()
    role_name = CharField(null=True)
    role_type = CharField(constraints=[SQL("DEFAULT '0'")])
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    tree_level = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    user_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'api_role'
        indexes = (
            (('parent_id', 'sort_order'), False),
        )

class ApiRule(BaseModel):
    api_permission = CharField(null=True)
    api_privileges = CharField(null=True)
    assert_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    resource_id = CharField(null=True)
    role = ForeignKeyField(column_name='role_id', constraints=[SQL("DEFAULT 0")], field='role_id', model=ApiRole)
    role_type = CharField(null=True)
    rule_id = AutoField()

    class Meta:
        table_name = 'api_rule'
        indexes = (
            (('resource_id', 'role'), False),
            (('role', 'resource_id'), False),
        )

class ApiUser(BaseModel):
    api_key = CharField(null=True)
    created = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    email = CharField(null=True)
    firstname = CharField(null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")])
    lastname = CharField(null=True)
    lognum = IntegerField(constraints=[SQL("DEFAULT 0")])
    modified = DateTimeField(null=True)
    reload_acl_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    user_id = AutoField()
    username = CharField(null=True)

    class Meta:
        table_name = 'api_user'

class ApiSession(BaseModel):
    logdate = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    sessid = CharField(index=True, null=True)
    user = ForeignKeyField(column_name='user_id', field='user_id', model=ApiUser)

    class Meta:
        table_name = 'api_session'
        primary_key = False

class ReviewEntity(BaseModel):
    entity_code = CharField()
    entity_id = AutoField()

    class Meta:
        table_name = 'review_entity'

class ReviewStatus(BaseModel):
    status_code = CharField()
    status_id = AutoField()

    class Meta:
        table_name = 'review_status'

class Review(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=ReviewEntity)
    entity_pk_value = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    review_id = BigAutoField()
    status = ForeignKeyField(column_name='status_id', constraints=[SQL("DEFAULT 0")], field='status_id', model=ReviewStatus)

    class Meta:
        table_name = 'review'

class CoreWebsite(BaseModel):
    code = CharField(null=True, unique=True)
    default_group_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_default = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    name = CharField(null=True)
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    website_id = AutoField()

    class Meta:
        table_name = 'core_website'

class CoreStoreGroup(BaseModel):
    default_store_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    group_id = AutoField()
    name = CharField()
    root_category_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    website = ForeignKeyField(column_name='website_id', constraints=[SQL("DEFAULT 0")], field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'core_store_group'

class CoreStore(BaseModel):
    code = CharField(null=True, unique=True)
    group = ForeignKeyField(column_name='group_id', constraints=[SQL("DEFAULT 0")], field='group_id', model=CoreStoreGroup)
    is_active = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField()
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    store_id = AutoField()
    website = ForeignKeyField(column_name='website_id', constraints=[SQL("DEFAULT 0")], field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'core_store'
        indexes = (
            (('is_active', 'sort_order'), False),
        )

class AwAdvancedreviewsAbuse(BaseModel):
    abused_at = DateTimeField()
    customer_id = IntegerField()
    customer_name = CharField(constraints=[SQL("DEFAULT ''")])
    id = BigAutoField()
    review = ForeignKeyField(column_name='review_id', field='review_id', model=Review)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)

    class Meta:
        table_name = 'aw_advancedreviews_abuse'

class AwAdvancedreviewsHelpfulness(BaseModel):
    customer_id = IntegerField()
    id = BigAutoField()
    review = ForeignKeyField(column_name='review_id', field='review_id', model=Review)
    value = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'aw_advancedreviews_helpfulness'

class AwAdvancedreviewsPc(BaseModel):
    id = BigAutoField()
    name = CharField(constraints=[SQL("DEFAULT ''")])
    owner = IntegerField()
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    status = IntegerField()
    type = IntegerField()

    class Meta:
        table_name = 'aw_advancedreviews_pc'

class AwAdvancedreviewsPcStore(BaseModel):
    proscons = ForeignKeyField(column_name='proscons_id', field='id', model=AwAdvancedreviewsPc)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)

    class Meta:
        table_name = 'aw_advancedreviews_pc_store'
        indexes = (
            (('proscons', 'store'), True),
        )
        primary_key = CompositeKey('proscons', 'store')

class AwAdvancedreviewsPcVote(BaseModel):
    id = BigIntegerField()
    proscons = ForeignKeyField(column_name='proscons_id', field='id', model=AwAdvancedreviewsPc)
    review = ForeignKeyField(column_name='review_id', field='review_id', model=Review)

    class Meta:
        table_name = 'aw_advancedreviews_pc_vote'
        indexes = (
            (('id', 'review', 'proscons'), True),
        )
        primary_key = CompositeKey('id', 'proscons', 'review')

class AwAdvancedreviewsRecommend(BaseModel):
    id = BigAutoField()
    review = ForeignKeyField(column_name='review_id', field='review_id', model=Review)
    value = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'aw_advancedreviews_recommend'

class AwAjaxcartproPromo(BaseModel):
    conditions_serialized = TextField(null=True)
    customer_groups = CharField()
    description = TextField(null=True)
    from_date = DateField(null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    name = CharField()
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    rule_actions_serialized = TextField(null=True)
    rule_id = AutoField()
    store_ids = CharField(constraints=[SQL("DEFAULT '0'")])
    to_date = DateField(null=True)
    type = IntegerField()

    class Meta:
        table_name = 'aw_ajaxcartpro_promo'

class CaptchaLog(BaseModel):
    count = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField()
    updated_at = DateTimeField(null=True)
    value = CharField()

    class Meta:
        table_name = 'captcha_log'
        indexes = (
            (('type', 'value'), True),
        )
        primary_key = CompositeKey('type', 'value')

class CatAssoc(BaseModel):
    category = CharField(null=True)
    live_catid = IntegerField(index=True, null=True)
    old_catid = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'cat_assoc'

class CatalogCategoryAncCategsIndexIdx(BaseModel):
    category_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    path = CharField(null=True)

    class Meta:
        table_name = 'catalog_category_anc_categs_index_idx'
        indexes = (
            (('path', 'category_id'), False),
        )
        primary_key = False

class CatalogCategoryAncCategsIndexTmp(BaseModel):
    category_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    path = CharField(null=True)

    class Meta:
        table_name = 'catalog_category_anc_categs_index_tmp'
        indexes = (
            (('path', 'category_id'), False),
        )
        primary_key = False

class CatalogCategoryAncProductsIndexIdx(BaseModel):
    category_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    position = IntegerField(null=True)
    product_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'catalog_category_anc_products_index_idx'
        indexes = (
            (('category_id', 'product_id', 'position'), False),
        )
        primary_key = False

class CatalogCategoryAncProductsIndexTmp(BaseModel):
    category_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    position = IntegerField(null=True)
    product_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'catalog_category_anc_products_index_tmp'
        indexes = (
            (('category_id', 'product_id', 'position'), False),
        )
        primary_key = False

class CatalogCategoryEntity(BaseModel):
    attribute_set_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    children_count = IntegerField()
    created_at = DateTimeField(null=True)
    entity_id = AutoField()
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    level = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    parent_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    path = CharField()
    position = IntegerField()
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'catalog_category_entity'
        indexes = (
            (('path', 'entity_id'), False),
        )

class EavEntityType(BaseModel):
    additional_attribute_table = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    attribute_model = CharField(null=True)
    data_sharing_key = CharField(constraints=[SQL("DEFAULT 'default'")], null=True)
    default_attribute_set_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    entity_attribute_collection = CharField(null=True)
    entity_id_field = CharField(null=True)
    entity_model = CharField()
    entity_table = CharField(null=True)
    entity_type_code = CharField(index=True)
    entity_type_id = AutoField()
    increment_model = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    increment_pad_char = CharField(constraints=[SQL("DEFAULT '0'")])
    increment_pad_length = IntegerField(constraints=[SQL("DEFAULT 8")])
    increment_per_store = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_data_sharing = IntegerField(constraints=[SQL("DEFAULT 1")])
    value_table_prefix = CharField(null=True)

    class Meta:
        table_name = 'eav_entity_type'

class EavAttribute(BaseModel):
    attribute_code = CharField(null=True)
    attribute_id = AutoField()
    attribute_model = CharField(null=True)
    backend_model = CharField(null=True)
    backend_table = CharField(null=True)
    backend_type = CharField(constraints=[SQL("DEFAULT 'static'")])
    default_value = TextField(null=True)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    frontend_class = CharField(null=True)
    frontend_input = CharField(null=True)
    frontend_label = CharField(null=True)
    frontend_model = CharField(null=True)
    is_required = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_unique = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_user_defined = IntegerField(constraints=[SQL("DEFAULT 0")])
    note = CharField(null=True)
    source_model = CharField(null=True)

    class Meta:
        table_name = 'eav_attribute'
        indexes = (
            (('entity_type', 'attribute_code'), True),
        )

class CatalogCategoryEntityDatetime(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogCategoryEntity)
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = DateTimeField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_category_entity_datetime'
        indexes = (
            (('entity_type_id', 'entity', 'attribute', 'store'), True),
        )

class CatalogCategoryEntityDecimal(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogCategoryEntity)
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = DecimalField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_category_entity_decimal'
        indexes = (
            (('entity_type_id', 'entity', 'attribute', 'store'), True),
        )

class CatalogCategoryEntityInt(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogCategoryEntity)
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = IntegerField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_category_entity_int'
        indexes = (
            (('entity_type_id', 'entity', 'attribute', 'store'), True),
        )

class CatalogCategoryEntityText(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogCategoryEntity)
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = TextField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_category_entity_text'
        indexes = (
            (('entity_type_id', 'entity', 'attribute', 'store'), True),
        )

class CatalogCategoryEntityVarchar(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogCategoryEntity)
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = CharField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_category_entity_varchar'
        indexes = (
            (('entity_type_id', 'entity', 'attribute', 'store'), True),
        )

class CatalogCategoryFlatStore1(BaseModel):
    all_children = TextField(null=True)
    available_sort_by = TextField(null=True)
    canonical_link = CharField(null=True)
    category_type = IntegerField(null=True)
    children = TextField(null=True)
    children_count = IntegerField()
    created_at = DateTimeField(null=True)
    custom_apply_to_products = IntegerField(null=True)
    custom_design = CharField(null=True)
    custom_design_from = DateTimeField(null=True)
    custom_design_to = DateTimeField(null=True)
    custom_layout_update = TextField(null=True)
    custom_use_parent_settings = IntegerField(null=True)
    default_sort_by = CharField(null=True)
    description = TextField(null=True)
    display_mode = CharField(null=True)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=CatalogCategoryEntity, primary_key=True)
    featured = IntegerField(null=True)
    featured_product_color = CharField(null=True)
    featured_product_limit = CharField(null=True)
    featured_text = TextField(null=True)
    featured_title = CharField(null=True)
    filter_price_range = DecimalField(null=True)
    hot_new_theme = IntegerField(null=True)
    hot_new_theme_homepage = IntegerField(null=True)
    hotnew_image = CharField(null=True)
    hotnew_image_mobile = CharField(null=True)
    hotnew_sort = CharField(null=True)
    image = CharField(null=True)
    include_in_menu = IntegerField(null=True)
    is_active = IntegerField(null=True)
    is_anchor = IntegerField(null=True)
    landing_page = IntegerField(null=True)
    landingpage_columns = IntegerField(null=True)
    level = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    menu_hot_new = TextField(null=True)
    menu_image = CharField(null=True)
    menu_image_url = CharField(null=True)
    menu_type = IntegerField(null=True)
    meta_description = TextField(null=True)
    meta_keywords = TextField(null=True)
    meta_title = CharField(null=True)
    name = CharField(null=True)
    notify = IntegerField(null=True)
    notify_code = CharField(null=True)
    page_layout = CharField(null=True)
    parent_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    partyitem_category = IntegerField(null=True)
    path = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    path_in_store = TextField(null=True)
    position = IntegerField()
    slideshow = IntegerField(null=True)
    slideshow_color = CharField(null=True)
    slideshow_image = CharField(null=True)
    slideshow_label = CharField(null=True)
    slideshow_order = CharField(null=True)
    slideshow_text = TextField(null=True)
    slideshow_thumbnail = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    theme_color = CharField(null=True)
    thumbnail = CharField(null=True)
    updated_at = DateTimeField(null=True)
    url_key = CharField(null=True)
    url_path = CharField(null=True)

    class Meta:
        table_name = 'catalog_category_flat_store_1'

class EavAttributeSet(BaseModel):
    attribute_set_id = AutoField()
    attribute_set_name = CharField(null=True)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'eav_attribute_set'
        indexes = (
            (('entity_type', 'attribute_set_name'), True),
            (('entity_type', 'sort_order'), False),
        )

class CatalogProductEntity(BaseModel):
    attribute_set = ForeignKeyField(column_name='attribute_set_id', constraints=[SQL("DEFAULT 0")], field='attribute_set_id', model=EavAttributeSet)
    created_at = DateTimeField(null=True)
    entity_id = AutoField()
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    has_options = IntegerField(constraints=[SQL("DEFAULT 0")])
    required_options = IntegerField(constraints=[SQL("DEFAULT 0")])
    sku = CharField(index=True, null=True)
    type_id = CharField(constraints=[SQL("DEFAULT 'simple'")])
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'catalog_product_entity'

class CatalogCategoryProduct(BaseModel):
    category = ForeignKeyField(column_name='category_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogCategoryEntity)
    position = IntegerField(constraints=[SQL("DEFAULT 0")])
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)

    class Meta:
        table_name = 'catalog_category_product'
        indexes = (
            (('category', 'product'), True),
        )
        primary_key = CompositeKey('category', 'product')

class CatalogCategoryProductIndex(BaseModel):
    category = ForeignKeyField(column_name='category_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogCategoryEntity)
    is_parent = IntegerField(constraints=[SQL("DEFAULT 0")])
    position = IntegerField(null=True)
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    visibility = IntegerField()

    class Meta:
        table_name = 'catalog_category_product_index'
        indexes = (
            (('category', 'product', 'store'), True),
            (('product', 'store', 'category', 'visibility'), False),
            (('store', 'category', 'visibility', 'is_parent', 'position'), False),
        )
        primary_key = CompositeKey('category', 'product', 'store')

class CatalogCategoryProductIndexEnblIdx(BaseModel):
    product_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    visibility = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'catalog_category_product_index_enbl_idx'
        indexes = (
            (('product_id', 'visibility'), False),
        )
        primary_key = False

class CatalogCategoryProductIndexEnblTmp(BaseModel):
    product_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    visibility = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'catalog_category_product_index_enbl_tmp'
        indexes = (
            (('product_id', 'visibility'), False),
        )
        primary_key = False

class CatalogCategoryProductIndexIdx(BaseModel):
    category_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_parent = IntegerField(constraints=[SQL("DEFAULT 0")])
    position = IntegerField(constraints=[SQL("DEFAULT 0")])
    product_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    visibility = IntegerField()

    class Meta:
        table_name = 'catalog_category_product_index_idx'
        indexes = (
            (('product_id', 'category_id', 'store_id'), False),
        )
        primary_key = False

class CatalogCategoryProductIndexTmp(BaseModel):
    category_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_parent = IntegerField(constraints=[SQL("DEFAULT 0")])
    position = IntegerField(constraints=[SQL("DEFAULT 0")])
    product_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    visibility = IntegerField()

    class Meta:
        table_name = 'catalog_category_product_index_tmp'
        indexes = (
            (('product_id', 'category_id', 'store_id'), False),
        )
        primary_key = False

class CustomerEntity(BaseModel):
    attribute_set_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    disable_auto_group_change = IntegerField(constraints=[SQL("DEFAULT 0")])
    email = CharField(null=True)
    entity_id = AutoField()
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    group_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    increment_id = CharField(null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore, null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite, null=True)

    class Meta:
        table_name = 'customer_entity'
        indexes = (
            (('email', 'website'), False),
            (('email', 'website'), True),
        )

class CatalogCompareItem(BaseModel):
    catalog_compare_item_id = AutoField()
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity, null=True)
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    visitor_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'catalog_compare_item'
        indexes = (
            (('customer', 'product'), False),
            (('visitor_id', 'product'), False),
        )

class CatalogEavAttribute(BaseModel):
    apply_to = CharField(null=True)
    attribute = ForeignKeyField(column_name='attribute_id', field='attribute_id', model=EavAttribute, primary_key=True)
    can_configure_import = IntegerField(constraints=[SQL("DEFAULT 1")])
    can_configure_inheritance = IntegerField(constraints=[SQL("DEFAULT 1")])
    frontend_input_renderer = CharField(null=True)
    import_to_dfw = IntegerField(constraints=[SQL("DEFAULT 1")])
    inheritance = IntegerField(constraints=[SQL("DEFAULT 1")])
    is_comparable = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_configurable = IntegerField(constraints=[SQL("DEFAULT 1")])
    is_filterable = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_filterable_in_search = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_global = IntegerField(constraints=[SQL("DEFAULT 1")])
    is_html_allowed_on_front = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_searchable = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_used_for_price_rules = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_used_for_promo_rules = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_visible = IntegerField(constraints=[SQL("DEFAULT 1")])
    is_visible_in_advanced_search = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_visible_on_front = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_wysiwyg_enabled = IntegerField(constraints=[SQL("DEFAULT 0")])
    position = IntegerField(constraints=[SQL("DEFAULT 0")])
    solr_boost = FloatField(constraints=[SQL("DEFAULT 1.0000")])
    used_for_sort_by = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    used_in_product_listing = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'catalog_eav_attribute'

class CatalogProductBundleOption(BaseModel):
    option_id = AutoField()
    parent = ForeignKeyField(column_name='parent_id', field='entity_id', model=CatalogProductEntity)
    position = IntegerField(constraints=[SQL("DEFAULT 0")])
    required = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField(null=True)

    class Meta:
        table_name = 'catalog_product_bundle_option'

class CatalogProductBundleOptionValue(BaseModel):
    option = ForeignKeyField(column_name='option_id', field='option_id', model=CatalogProductBundleOption)
    store_id = IntegerField()
    title = CharField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_product_bundle_option_value'
        indexes = (
            (('option', 'store_id'), True),
        )

class CustomerGroup(BaseModel):
    customer_group_code = CharField()
    customer_group_id = AutoField()
    tax_class_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'customer_group'

class CatalogProductBundlePriceIndex(BaseModel):
    customer_group = ForeignKeyField(column_name='customer_group_id', field='customer_group_id', model=CustomerGroup)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=CatalogProductEntity)
    max_price = DecimalField()
    min_price = DecimalField()
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalog_product_bundle_price_index'
        indexes = (
            (('entity', 'website', 'customer_group'), True),
        )
        primary_key = CompositeKey('customer_group', 'entity', 'website')

class CatalogProductBundleSelection(BaseModel):
    is_default = IntegerField(constraints=[SQL("DEFAULT 0")])
    option = ForeignKeyField(column_name='option_id', field='option_id', model=CatalogProductBundleOption)
    parent_product_id = IntegerField()
    position = IntegerField(constraints=[SQL("DEFAULT 0")])
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity)
    selection_can_change_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    selection_id = AutoField()
    selection_price_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    selection_price_value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    selection_qty = DecimalField(null=True)

    class Meta:
        table_name = 'catalog_product_bundle_selection'

class CatalogProductBundleSelectionPrice(BaseModel):
    selection = ForeignKeyField(column_name='selection_id', field='selection_id', model=CatalogProductBundleSelection)
    selection_price_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    selection_price_value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalog_product_bundle_selection_price'
        indexes = (
            (('selection', 'website'), True),
        )
        primary_key = CompositeKey('selection', 'website')

class CatalogProductBundleStockIndex(BaseModel):
    entity_id = IntegerField()
    option_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    stock_id = IntegerField()
    stock_status = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_bundle_stock_index'
        indexes = (
            (('entity_id', 'website_id', 'stock_id', 'option_id'), True),
        )
        primary_key = CompositeKey('entity_id', 'option_id', 'stock_id', 'website_id')

class CatalogProductEnabledIndex(BaseModel):
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    visibility = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'catalog_product_enabled_index'
        indexes = (
            (('product', 'store'), True),
        )
        primary_key = CompositeKey('product', 'store')

class CatalogProductEntityDatetime(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = DateTimeField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_product_entity_datetime'
        indexes = (
            (('entity', 'attribute', 'store'), True),
        )

class CatalogProductEntityDecimal(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = DecimalField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_product_entity_decimal'
        indexes = (
            (('entity', 'attribute', 'store'), True),
        )

class CatalogProductEntityGallery(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    position = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = CharField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_product_entity_gallery'
        indexes = (
            (('entity_type_id', 'entity', 'attribute', 'store'), True),
        )

class CatalogProductEntityGroupPrice(BaseModel):
    all_groups = IntegerField(constraints=[SQL("DEFAULT 1")])
    customer_group = ForeignKeyField(column_name='customer_group_id', constraints=[SQL("DEFAULT 0")], field='customer_group_id', model=CustomerGroup)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    is_percent = IntegerField(constraints=[SQL("DEFAULT 0")])
    value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    value_id = AutoField()
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalog_product_entity_group_price'
        indexes = (
            (('entity', 'all_groups', 'customer_group', 'website'), True),
        )

class CatalogProductEntityInt(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = IntegerField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_product_entity_int'
        indexes = (
            (('entity', 'attribute', 'store'), True),
        )

class CatalogProductEntityMediaGallery(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    value = CharField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_product_entity_media_gallery'

class CatalogProductEntityMediaGalleryValue(BaseModel):
    disabled = IntegerField(constraints=[SQL("DEFAULT 0")])
    label = CharField(null=True)
    position = IntegerField(null=True)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = ForeignKeyField(column_name='value_id', constraints=[SQL("DEFAULT 0")], field='value_id', model=CatalogProductEntityMediaGallery)

    class Meta:
        table_name = 'catalog_product_entity_media_gallery_value'
        indexes = (
            (('value', 'store'), True),
        )
        primary_key = CompositeKey('store', 'value')

class CatalogProductEntityText(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = TextField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_product_entity_text'
        indexes = (
            (('entity', 'attribute', 'store'), True),
        )

class CatalogProductEntityTierPrice(BaseModel):
    all_groups = IntegerField(constraints=[SQL("DEFAULT 1")])
    customer_group = ForeignKeyField(column_name='customer_group_id', constraints=[SQL("DEFAULT 0")], field='customer_group_id', model=CustomerGroup)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    qty = DecimalField(constraints=[SQL("DEFAULT 1.0000")])
    value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    value_id = AutoField()
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalog_product_entity_tier_price'
        indexes = (
            (('entity', 'all_groups', 'customer_group', 'qty', 'website'), True),
        )

class CatalogProductEntityVarchar(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = CharField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_product_entity_varchar'
        indexes = (
            (('entity', 'attribute', 'store'), True),
        )

class CatalogProductFlat1(BaseModel):
    attribute_set_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    button_type = IntegerField(null=True)
    button_type_value = CharField(null=True)
    cost = DecimalField(null=True)
    created_at = DateTimeField(null=True)
    creative_fancy_tableware = IntegerField(null=True)
    creative_fancy_tableware_value = CharField(null=True)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=CatalogProductEntity, primary_key=True)
    gift_message_available = IntegerField(null=True)
    has_options = IntegerField(constraints=[SQL("DEFAULT 0")])
    image = CharField(null=True)
    image_label = CharField(null=True)
    is_imported = IntegerField(null=True)
    is_imported_value = CharField(null=True)
    is_recurring = IntegerField(null=True)
    item_type = IntegerField(index=True, null=True)
    item_type_value = CharField(index=True, null=True)
    line_type = CharField(index=True, null=True)
    links_exist = IntegerField(null=True)
    links_purchased_separately = IntegerField(null=True)
    links_title = CharField(null=True)
    msrp = DecimalField(null=True)
    msrp_display_actual_price_type = CharField(null=True)
    msrp_enabled = IntegerField(null=True)
    name = CharField(index=True, null=True)
    news_from_date = DateTimeField(null=True)
    news_to_date = DateTimeField(null=True)
    plp = IntegerField(null=True)
    price = DecimalField(index=True, null=True)
    price_type = IntegerField(null=True)
    price_view = IntegerField(null=True)
    recurring_profile = TextField(null=True)
    required_options = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipment_type = IntegerField(null=True)
    short_description = TextField(null=True)
    sku = CharField(null=True)
    sku_type = IntegerField(null=True)
    small_image = CharField(null=True)
    small_image_label = CharField(null=True)
    special_from_date = DateTimeField(null=True)
    special_price = DecimalField(null=True)
    special_to_date = DateTimeField(null=True)
    status = IntegerField(index=True, null=True)
    tax_class_id = IntegerField(null=True)
    thumbnail = CharField(null=True)
    thumbnail_label = CharField(null=True)
    type_id = CharField(constraints=[SQL("DEFAULT 'simple'")], index=True)
    updated_at = DateTimeField(null=True)
    url_key = CharField(null=True)
    url_path = CharField(null=True)
    visibility = IntegerField(null=True)
    weight = DecimalField(null=True)
    weight_type = IntegerField(null=True)

    class Meta:
        table_name = 'catalog_product_flat_1'

class CatalogProductFlat2(BaseModel):
    attribute_set_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    button_type = IntegerField(null=True)
    button_type_value = CharField(null=True)
    cost = DecimalField(null=True)
    created_at = DateTimeField(null=True)
    creative_fancy_tableware = IntegerField(null=True)
    creative_fancy_tableware_value = CharField(null=True)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=CatalogProductEntity, primary_key=True)
    gift_message_available = IntegerField(null=True)
    has_options = IntegerField(constraints=[SQL("DEFAULT 0")])
    image = CharField(null=True)
    image_label = CharField(null=True)
    is_imported = IntegerField(null=True)
    is_imported_value = CharField(null=True)
    is_recurring = IntegerField(null=True)
    item_type = IntegerField(index=True, null=True)
    item_type_value = CharField(index=True, null=True)
    line_type = CharField(index=True, null=True)
    links_exist = IntegerField(null=True)
    links_purchased_separately = IntegerField(null=True)
    links_title = CharField(null=True)
    msrp = DecimalField(null=True)
    msrp_display_actual_price_type = CharField(null=True)
    msrp_enabled = IntegerField(null=True)
    name = CharField(index=True, null=True)
    news_from_date = DateTimeField(null=True)
    news_to_date = DateTimeField(null=True)
    plp = IntegerField(null=True)
    price = DecimalField(index=True, null=True)
    price_type = IntegerField(null=True)
    price_view = IntegerField(null=True)
    recurring_profile = TextField(null=True)
    required_options = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipment_type = IntegerField(null=True)
    short_description = TextField(null=True)
    sku = CharField(null=True)
    sku_type = IntegerField(null=True)
    small_image = CharField(null=True)
    small_image_label = CharField(null=True)
    special_from_date = DateTimeField(null=True)
    special_price = DecimalField(null=True)
    special_to_date = DateTimeField(null=True)
    status = IntegerField(index=True, null=True)
    tax_class_id = IntegerField(null=True)
    thumbnail = CharField(null=True)
    thumbnail_label = CharField(null=True)
    type_id = CharField(constraints=[SQL("DEFAULT 'simple'")], index=True)
    updated_at = DateTimeField(null=True)
    url_key = CharField(null=True)
    url_path = CharField(null=True)
    visibility = IntegerField(null=True)
    weight = DecimalField(null=True)
    weight_type = IntegerField(null=True)

    class Meta:
        table_name = 'catalog_product_flat_2'

class CatalogProductIndexEav(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=CatalogProductEntity)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore)
    value = IntegerField(index=True)

    class Meta:
        table_name = 'catalog_product_index_eav'
        indexes = (
            (('entity', 'attribute', 'store', 'value'), True),
        )
        primary_key = CompositeKey('attribute', 'entity', 'store', 'value')

class CatalogProductIndexEavDecimal(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=CatalogProductEntity)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore)
    value = DecimalField(index=True)

    class Meta:
        table_name = 'catalog_product_index_eav_decimal'
        indexes = (
            (('entity', 'attribute', 'store'), True),
        )
        primary_key = CompositeKey('attribute', 'entity', 'store')

class CatalogProductIndexEavDecimalIdx(BaseModel):
    attribute_id = IntegerField(index=True)
    entity_id = IntegerField(index=True)
    store_id = IntegerField(index=True)
    value = DecimalField(index=True)

    class Meta:
        table_name = 'catalog_product_index_eav_decimal_idx'
        indexes = (
            (('entity_id', 'attribute_id', 'store_id', 'value'), True),
        )
        primary_key = CompositeKey('attribute_id', 'entity_id', 'store_id', 'value')

class CatalogProductIndexEavDecimalTmp(BaseModel):
    attribute_id = IntegerField(index=True)
    entity_id = IntegerField(index=True)
    store_id = IntegerField(index=True)
    value = DecimalField(index=True)

    class Meta:
        table_name = 'catalog_product_index_eav_decimal_tmp'
        indexes = (
            (('entity_id', 'attribute_id', 'store_id'), True),
        )
        primary_key = CompositeKey('attribute_id', 'entity_id', 'store_id')

class CatalogProductIndexEavIdx(BaseModel):
    attribute_id = IntegerField(index=True)
    entity_id = IntegerField(index=True)
    store_id = IntegerField(index=True)
    value = IntegerField(index=True)

    class Meta:
        table_name = 'catalog_product_index_eav_idx'
        indexes = (
            (('entity_id', 'attribute_id', 'store_id', 'value'), True),
        )
        primary_key = CompositeKey('attribute_id', 'entity_id', 'store_id', 'value')

class CatalogProductIndexEavTmp(BaseModel):
    attribute_id = IntegerField(index=True)
    entity_id = IntegerField(index=True)
    store_id = IntegerField(index=True)
    value = IntegerField(index=True)

    class Meta:
        table_name = 'catalog_product_index_eav_tmp'
        indexes = (
            (('entity_id', 'attribute_id', 'store_id', 'value'), True),
        )
        primary_key = CompositeKey('attribute_id', 'entity_id', 'store_id', 'value')

class CatalogProductIndexGroupPrice(BaseModel):
    customer_group = ForeignKeyField(column_name='customer_group_id', field='customer_group_id', model=CustomerGroup)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=CatalogProductEntity)
    price = DecimalField(null=True)
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalog_product_index_group_price'
        indexes = (
            (('entity', 'customer_group', 'website'), True),
        )
        primary_key = CompositeKey('customer_group', 'entity', 'website')

class CatalogProductIndexPrice(BaseModel):
    customer_group = ForeignKeyField(column_name='customer_group_id', field='customer_group_id', model=CustomerGroup)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=CatalogProductEntity)
    final_price = DecimalField(null=True)
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(index=True, null=True)
    price = DecimalField(null=True)
    tax_class_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    tier_price = DecimalField(null=True)
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalog_product_index_price'
        indexes = (
            (('entity', 'customer_group', 'website'), True),
            (('website', 'customer_group', 'min_price'), False),
        )
        primary_key = CompositeKey('customer_group', 'entity', 'website')

class CatalogProductIndexPriceBundleIdx(BaseModel):
    base_group_price = DecimalField(null=True)
    base_tier = DecimalField(null=True)
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    group_price_percent = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(null=True)
    orig_price = DecimalField(null=True)
    price = DecimalField(null=True)
    price_type = IntegerField()
    special_price = DecimalField(null=True)
    tax_class_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    tier_percent = DecimalField(null=True)
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_bundle_idx'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'website_id')

class CatalogProductIndexPriceBundleOptIdx(BaseModel):
    alt_group_price = DecimalField(null=True)
    alt_price = DecimalField(null=True)
    alt_tier_price = DecimalField(null=True)
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(null=True)
    option_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_bundle_opt_idx'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id', 'option_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'option_id', 'website_id')

class CatalogProductIndexPriceBundleOptTmp(BaseModel):
    alt_group_price = DecimalField(null=True)
    alt_price = DecimalField(null=True)
    alt_tier_price = DecimalField(null=True)
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(null=True)
    option_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_bundle_opt_tmp'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id', 'option_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'option_id', 'website_id')

class CatalogProductIndexPriceBundleSelIdx(BaseModel):
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    group_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    is_required = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    option_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    price = DecimalField(null=True)
    selection_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_bundle_sel_idx'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id', 'option_id', 'selection_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'option_id', 'selection_id', 'website_id')

class CatalogProductIndexPriceBundleSelTmp(BaseModel):
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    group_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    is_required = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    option_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    price = DecimalField(null=True)
    selection_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_bundle_sel_tmp'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id', 'option_id', 'selection_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'option_id', 'selection_id', 'website_id')

class CatalogProductIndexPriceBundleTmp(BaseModel):
    base_group_price = DecimalField(null=True)
    base_tier = DecimalField(null=True)
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    group_price_percent = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(null=True)
    orig_price = DecimalField(null=True)
    price = DecimalField(null=True)
    price_type = IntegerField()
    special_price = DecimalField(null=True)
    tax_class_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    tier_percent = DecimalField(null=True)
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_bundle_tmp'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'website_id')

class CatalogProductIndexPriceCfgOptAgrIdx(BaseModel):
    child_id = IntegerField()
    customer_group_id = IntegerField()
    group_price = DecimalField(null=True)
    parent_id = IntegerField()
    price = DecimalField(null=True)
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_cfg_opt_agr_idx'
        indexes = (
            (('parent_id', 'child_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('child_id', 'customer_group_id', 'parent_id', 'website_id')

class CatalogProductIndexPriceCfgOptAgrTmp(BaseModel):
    child_id = IntegerField()
    customer_group_id = IntegerField()
    group_price = DecimalField(null=True)
    parent_id = IntegerField()
    price = DecimalField(null=True)
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_cfg_opt_agr_tmp'
        indexes = (
            (('parent_id', 'child_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('child_id', 'customer_group_id', 'parent_id', 'website_id')

class CatalogProductIndexPriceCfgOptIdx(BaseModel):
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(null=True)
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_cfg_opt_idx'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'website_id')

class CatalogProductIndexPriceCfgOptTmp(BaseModel):
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(null=True)
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_cfg_opt_tmp'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'website_id')

class CatalogProductIndexPriceDownlodIdx(BaseModel):
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    max_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    min_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_downlod_idx'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'website_id')

class CatalogProductIndexPriceDownlodTmp(BaseModel):
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    max_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    min_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_downlod_tmp'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'website_id')

class CatalogProductIndexPriceFinalIdx(BaseModel):
    base_group_price = DecimalField(null=True)
    base_tier = DecimalField(null=True)
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(null=True)
    orig_price = DecimalField(null=True)
    price = DecimalField(null=True)
    tax_class_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_final_idx'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'website_id')

class CatalogProductIndexPriceFinalTmp(BaseModel):
    base_group_price = DecimalField(null=True)
    base_tier = DecimalField(null=True)
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(null=True)
    orig_price = DecimalField(null=True)
    price = DecimalField(null=True)
    tax_class_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_final_tmp'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'website_id')

class CatalogProductIndexPriceIdx(BaseModel):
    customer_group_id = IntegerField(index=True)
    entity_id = IntegerField()
    final_price = DecimalField(null=True)
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(index=True, null=True)
    price = DecimalField(null=True)
    tax_class_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    tier_price = DecimalField(null=True)
    website_id = IntegerField(index=True)

    class Meta:
        table_name = 'catalog_product_index_price_idx'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'website_id')

class CatalogProductIndexPriceOptAgrIdx(BaseModel):
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(null=True)
    option_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_opt_agr_idx'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id', 'option_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'option_id', 'website_id')

class CatalogProductIndexPriceOptAgrTmp(BaseModel):
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(null=True)
    option_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_opt_agr_tmp'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id', 'option_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'option_id', 'website_id')

class CatalogProductIndexPriceOptIdx(BaseModel):
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(null=True)
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_opt_idx'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'website_id')

class CatalogProductIndexPriceOptTmp(BaseModel):
    customer_group_id = IntegerField()
    entity_id = IntegerField()
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(null=True)
    tier_price = DecimalField(null=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'catalog_product_index_price_opt_tmp'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'website_id')

class CatalogProductIndexPriceTmp(BaseModel):
    customer_group_id = IntegerField(index=True)
    entity_id = IntegerField()
    final_price = DecimalField(null=True)
    group_price = DecimalField(null=True)
    max_price = DecimalField(null=True)
    min_price = DecimalField(index=True, null=True)
    price = DecimalField(null=True)
    tax_class_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    tier_price = DecimalField(null=True)
    website_id = IntegerField(index=True)

    class Meta:
        table_name = 'catalog_product_index_price_tmp'
        indexes = (
            (('entity_id', 'customer_group_id', 'website_id'), True),
        )
        primary_key = CompositeKey('customer_group_id', 'entity_id', 'website_id')

class CatalogProductIndexTierPrice(BaseModel):
    customer_group = ForeignKeyField(column_name='customer_group_id', field='customer_group_id', model=CustomerGroup)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=CatalogProductEntity)
    min_price = DecimalField(null=True)
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalog_product_index_tier_price'
        indexes = (
            (('entity', 'customer_group', 'website'), True),
        )
        primary_key = CompositeKey('customer_group', 'entity', 'website')

class CatalogProductIndexWebsite(BaseModel):
    rate = FloatField(constraints=[SQL("DEFAULT 1")], null=True)
    website_date = DateField(index=True, null=True)
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite, primary_key=True)

    class Meta:
        table_name = 'catalog_product_index_website'

class CatalogProductLinkType(BaseModel):
    code = CharField(null=True)
    link_type_id = AutoField()

    class Meta:
        table_name = 'catalog_product_link_type'

class CatalogProductLink(BaseModel):
    link_id = AutoField()
    link_type = ForeignKeyField(column_name='link_type_id', constraints=[SQL("DEFAULT 0")], field='link_type_id', model=CatalogProductLinkType)
    linked_product = ForeignKeyField(column_name='linked_product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    product = ForeignKeyField(backref='catalog_product_entity_product_set', column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)

    class Meta:
        table_name = 'catalog_product_link'
        indexes = (
            (('link_type', 'product', 'linked_product'), True),
        )

class CatalogProductLinkAttribute(BaseModel):
    data_type = CharField(null=True)
    link_type = ForeignKeyField(column_name='link_type_id', constraints=[SQL("DEFAULT 0")], field='link_type_id', model=CatalogProductLinkType)
    product_link_attribute_code = CharField(null=True)
    product_link_attribute_id = AutoField()

    class Meta:
        table_name = 'catalog_product_link_attribute'

class CatalogProductLinkAttributeDecimal(BaseModel):
    link = ForeignKeyField(column_name='link_id', field='link_id', model=CatalogProductLink)
    product_link_attribute = ForeignKeyField(column_name='product_link_attribute_id', field='product_link_attribute_id', model=CatalogProductLinkAttribute, null=True)
    value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_product_link_attribute_decimal'
        indexes = (
            (('product_link_attribute', 'link'), True),
        )

class CatalogProductLinkAttributeInt(BaseModel):
    link = ForeignKeyField(column_name='link_id', field='link_id', model=CatalogProductLink)
    product_link_attribute = ForeignKeyField(column_name='product_link_attribute_id', field='product_link_attribute_id', model=CatalogProductLinkAttribute, null=True)
    value = IntegerField(constraints=[SQL("DEFAULT 0")])
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_product_link_attribute_int'
        indexes = (
            (('product_link_attribute', 'link'), True),
        )

class CatalogProductLinkAttributeVarchar(BaseModel):
    link = ForeignKeyField(column_name='link_id', field='link_id', model=CatalogProductLink)
    product_link_attribute = ForeignKeyField(column_name='product_link_attribute_id', constraints=[SQL("DEFAULT 0")], field='product_link_attribute_id', model=CatalogProductLinkAttribute)
    value = CharField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_product_link_attribute_varchar'
        indexes = (
            (('product_link_attribute', 'link'), True),
        )

class CatalogProductOption(BaseModel):
    file_extension = CharField(null=True)
    image_size_x = IntegerField(null=True)
    image_size_y = IntegerField(null=True)
    is_require = IntegerField(constraints=[SQL("DEFAULT 1")])
    max_characters = IntegerField(null=True)
    option_id = AutoField()
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    sku = CharField(null=True)
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField(null=True)

    class Meta:
        table_name = 'catalog_product_option'

class CatalogProductOptionPrice(BaseModel):
    option = ForeignKeyField(column_name='option_id', constraints=[SQL("DEFAULT 0")], field='option_id', model=CatalogProductOption)
    option_price_id = AutoField()
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    price_type = CharField(constraints=[SQL("DEFAULT 'fixed'")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)

    class Meta:
        table_name = 'catalog_product_option_price'
        indexes = (
            (('option', 'store'), True),
        )

class CatalogProductOptionTitle(BaseModel):
    option = ForeignKeyField(column_name='option_id', constraints=[SQL("DEFAULT 0")], field='option_id', model=CatalogProductOption)
    option_title_id = AutoField()
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    title = CharField(null=True)

    class Meta:
        table_name = 'catalog_product_option_title'
        indexes = (
            (('option', 'store'), True),
        )

class CatalogProductOptionTypeValue(BaseModel):
    option = ForeignKeyField(column_name='option_id', constraints=[SQL("DEFAULT 0")], field='option_id', model=CatalogProductOption)
    option_type_id = AutoField()
    sku = CharField(null=True)
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'catalog_product_option_type_value'

class CatalogProductOptionTypePrice(BaseModel):
    option_type = ForeignKeyField(column_name='option_type_id', constraints=[SQL("DEFAULT 0")], field='option_type_id', model=CatalogProductOptionTypeValue)
    option_type_price_id = AutoField()
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    price_type = CharField(constraints=[SQL("DEFAULT 'fixed'")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)

    class Meta:
        table_name = 'catalog_product_option_type_price'
        indexes = (
            (('option_type', 'store'), True),
        )

class CatalogProductOptionTypeTitle(BaseModel):
    option_type = ForeignKeyField(column_name='option_type_id', constraints=[SQL("DEFAULT 0")], field='option_type_id', model=CatalogProductOptionTypeValue)
    option_type_title_id = AutoField()
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    title = CharField(null=True)

    class Meta:
        table_name = 'catalog_product_option_type_title'
        indexes = (
            (('option_type', 'store'), True),
        )

class CatalogProductRelation(BaseModel):
    child = ForeignKeyField(column_name='child_id', field='entity_id', model=CatalogProductEntity)
    parent = ForeignKeyField(backref='catalog_product_entity_parent_set', column_name='parent_id', field='entity_id', model=CatalogProductEntity)

    class Meta:
        table_name = 'catalog_product_relation'
        indexes = (
            (('parent', 'child'), True),
        )
        primary_key = CompositeKey('child', 'parent')

class CatalogProductSuperAttribute(BaseModel):
    attribute_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    position = IntegerField(constraints=[SQL("DEFAULT 0")])
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    product_super_attribute_id = AutoField()

    class Meta:
        table_name = 'catalog_product_super_attribute'
        indexes = (
            (('product', 'attribute_id'), True),
        )

class CatalogProductSuperAttributeLabel(BaseModel):
    product_super_attribute = ForeignKeyField(column_name='product_super_attribute_id', constraints=[SQL("DEFAULT 0")], field='product_super_attribute_id', model=CatalogProductSuperAttribute)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    use_default = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    value = CharField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'catalog_product_super_attribute_label'
        indexes = (
            (('product_super_attribute', 'store'), True),
        )

class CatalogProductSuperAttributePricing(BaseModel):
    is_percent = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    pricing_value = DecimalField(null=True)
    product_super_attribute = ForeignKeyField(column_name='product_super_attribute_id', constraints=[SQL("DEFAULT 0")], field='product_super_attribute_id', model=CatalogProductSuperAttribute)
    value_id = AutoField()
    value_index = CharField(null=True)
    website = ForeignKeyField(column_name='website_id', constraints=[SQL("DEFAULT 0")], field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalog_product_super_attribute_pricing'
        indexes = (
            (('product_super_attribute', 'value_index', 'website'), True),
        )

class CatalogProductSuperLink(BaseModel):
    link_id = AutoField()
    parent = ForeignKeyField(column_name='parent_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    product = ForeignKeyField(backref='catalog_product_entity_product_set', column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)

    class Meta:
        table_name = 'catalog_product_super_link'
        indexes = (
            (('product', 'parent'), True),
        )

class CatalogProductWebsite(BaseModel):
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity)
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalog_product_website'
        indexes = (
            (('product', 'website'), True),
        )
        primary_key = CompositeKey('product', 'website')

class CataloginventoryStock(BaseModel):
    stock_id = AutoField()
    stock_name = CharField(null=True)

    class Meta:
        table_name = 'cataloginventory_stock'

class CataloginventoryStockItem(BaseModel):
    backorders = IntegerField(constraints=[SQL("DEFAULT 0")])
    enable_qty_increments = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_decimal_divided = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_in_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_qty_decimal = IntegerField(constraints=[SQL("DEFAULT 0")])
    item_id = AutoField()
    low_stock_date = DateTimeField(null=True)
    manage_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    max_sale_qty = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    min_qty = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    min_sale_qty = DecimalField(constraints=[SQL("DEFAULT 1.0000")])
    notify_stock_qty = DecimalField(null=True)
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    qty = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    qty_increments = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    stock = ForeignKeyField(column_name='stock_id', constraints=[SQL("DEFAULT 0")], field='stock_id', model=CataloginventoryStock)
    stock_status_changed_auto = IntegerField(constraints=[SQL("DEFAULT 0")])
    use_config_backorders = IntegerField(constraints=[SQL("DEFAULT 1")])
    use_config_enable_qty_inc = IntegerField(constraints=[SQL("DEFAULT 1")])
    use_config_manage_stock = IntegerField(constraints=[SQL("DEFAULT 1")])
    use_config_max_sale_qty = IntegerField(constraints=[SQL("DEFAULT 1")])
    use_config_min_qty = IntegerField(constraints=[SQL("DEFAULT 1")])
    use_config_min_sale_qty = IntegerField(constraints=[SQL("DEFAULT 1")])
    use_config_notify_stock_qty = IntegerField(constraints=[SQL("DEFAULT 1")])
    use_config_qty_increments = IntegerField(constraints=[SQL("DEFAULT 1")])

    class Meta:
        table_name = 'cataloginventory_stock_item'
        indexes = (
            (('product', 'stock'), True),
        )

class CataloginventoryStockStatus(BaseModel):
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity)
    qty = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    stock = ForeignKeyField(column_name='stock_id', field='stock_id', model=CataloginventoryStock)
    stock_status = IntegerField()
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'cataloginventory_stock_status'
        indexes = (
            (('product', 'website', 'stock'), True),
        )
        primary_key = CompositeKey('product', 'stock', 'website')

class CataloginventoryStockStatusIdx(BaseModel):
    product_id = IntegerField()
    qty = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    stock_id = IntegerField(index=True)
    stock_status = IntegerField()
    website_id = IntegerField(index=True)

    class Meta:
        table_name = 'cataloginventory_stock_status_idx'
        indexes = (
            (('product_id', 'website_id', 'stock_id'), True),
        )
        primary_key = CompositeKey('product_id', 'stock_id', 'website_id')

class CataloginventoryStockStatusTmp(BaseModel):
    product_id = IntegerField()
    qty = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    stock_id = IntegerField(index=True)
    stock_status = IntegerField()
    website_id = IntegerField(index=True)

    class Meta:
        table_name = 'cataloginventory_stock_status_tmp'
        indexes = (
            (('product_id', 'website_id', 'stock_id'), True),
        )
        primary_key = CompositeKey('product_id', 'stock_id', 'website_id')

class Catalogrule(BaseModel):
    actions_serialized = TextField(null=True)
    conditions_serialized = TextField(null=True)
    description = TextField(null=True)
    discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    from_date = DateField(null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField(null=True)
    rule_id = AutoField()
    simple_action = CharField(null=True)
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    stop_rules_processing = IntegerField(constraints=[SQL("DEFAULT 1")])
    sub_discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    sub_is_enable = IntegerField(constraints=[SQL("DEFAULT 0")])
    sub_simple_action = CharField(null=True)
    to_date = DateField(null=True)

    class Meta:
        table_name = 'catalogrule'
        indexes = (
            (('is_active', 'sort_order', 'to_date', 'from_date'), False),
        )

class CatalogruleAffectedProduct(BaseModel):
    product_id = AutoField()

    class Meta:
        table_name = 'catalogrule_affected_product'

class CatalogruleCustomerGroup(BaseModel):
    customer_group = ForeignKeyField(column_name='customer_group_id', field='customer_group_id', model=CustomerGroup)
    rule = ForeignKeyField(column_name='rule_id', field='rule_id', model=Catalogrule)

    class Meta:
        table_name = 'catalogrule_customer_group'
        indexes = (
            (('rule', 'customer_group'), True),
        )
        primary_key = CompositeKey('customer_group', 'rule')

class CatalogruleGroupWebsite(BaseModel):
    customer_group = ForeignKeyField(column_name='customer_group_id', constraints=[SQL("DEFAULT 0")], field='customer_group_id', model=CustomerGroup)
    rule = ForeignKeyField(column_name='rule_id', constraints=[SQL("DEFAULT 0")], field='rule_id', model=Catalogrule)
    website = ForeignKeyField(column_name='website_id', constraints=[SQL("DEFAULT 0")], field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalogrule_group_website'
        indexes = (
            (('rule', 'customer_group', 'website'), True),
        )
        primary_key = CompositeKey('customer_group', 'rule', 'website')

class CatalogruleProduct(BaseModel):
    action_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    action_operator = CharField(constraints=[SQL("DEFAULT 'to_fixed'")], null=True)
    action_stop = IntegerField(constraints=[SQL("DEFAULT 0")])
    customer_group = ForeignKeyField(column_name='customer_group_id', constraints=[SQL("DEFAULT 0")], field='customer_group_id', model=CustomerGroup)
    from_time = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    rule = ForeignKeyField(column_name='rule_id', constraints=[SQL("DEFAULT 0")], field='rule_id', model=Catalogrule)
    rule_product_id = AutoField()
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    sub_discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    sub_simple_action = CharField(null=True)
    to_time = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalogrule_product'
        indexes = (
            (('rule', 'from_time', 'to_time', 'website', 'customer_group', 'product', 'sort_order'), True),
        )

class CatalogruleProductPrice(BaseModel):
    customer_group = ForeignKeyField(column_name='customer_group_id', constraints=[SQL("DEFAULT 0")], field='customer_group_id', model=CustomerGroup)
    earliest_end_date = DateField(null=True)
    latest_start_date = DateField(null=True)
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    rule_date = DateField()
    rule_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    rule_product_price_id = AutoField()
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalogrule_product_price'
        indexes = (
            (('rule_date', 'website', 'customer_group', 'product'), True),
        )

class CatalogruleWebsite(BaseModel):
    rule = ForeignKeyField(column_name='rule_id', field='rule_id', model=Catalogrule)
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'catalogrule_website'
        indexes = (
            (('rule', 'website'), True),
        )
        primary_key = CompositeKey('rule', 'website')

class CatalogsearchFulltext(BaseModel):
    data_index = TextField(index=True, null=True)
    fulltext_id = AutoField()
    product_id = IntegerField()
    store_id = IntegerField()

    class Meta:
        table_name = 'catalogsearch_fulltext'
        indexes = (
            (('product_id', 'store_id'), True),
        )

class CatalogsearchQuery(BaseModel):
    display_in_terms = IntegerField(constraints=[SQL("DEFAULT 1")])
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    is_processed = IntegerField(constraints=[SQL("DEFAULT 0")], index=True, null=True)
    num_results = IntegerField(constraints=[SQL("DEFAULT 0")])
    popularity = IntegerField(constraints=[SQL("DEFAULT 0")])
    query_id = AutoField()
    query_text = CharField(null=True)
    redirect = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    synonym_for = CharField(index=True, null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])

    class Meta:
        table_name = 'catalogsearch_query'
        indexes = (
            (('query_text', 'store', 'popularity'), False),
        )

class CatalogsearchResult(BaseModel):
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity)
    query = ForeignKeyField(column_name='query_id', field='query_id', model=CatalogsearchQuery)
    relevance = DecimalField(constraints=[SQL("DEFAULT 0.0000")])

    class Meta:
        table_name = 'catalogsearch_result'
        indexes = (
            (('query', 'product'), True),
        )
        primary_key = CompositeKey('product', 'query')

class CheckoutAgreement(BaseModel):
    agreement_id = AutoField()
    checkbox_text = TextField(null=True)
    content = TextField(null=True)
    content_height = CharField(null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_html = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField(null=True)

    class Meta:
        table_name = 'checkout_agreement'

class CheckoutAgreementStore(BaseModel):
    agreement = ForeignKeyField(column_name='agreement_id', field='agreement_id', model=CheckoutAgreement)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore)

    class Meta:
        table_name = 'checkout_agreement_store'
        indexes = (
            (('agreement', 'store'), True),
        )
        primary_key = CompositeKey('agreement', 'store')

class CmsBlock(BaseModel):
    block_id = AutoField()
    content = TextField(null=True)
    creation_time = DateTimeField(null=True)
    identifier = CharField()
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")])
    title = CharField()
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'cms_block'

class CmsBlockStore(BaseModel):
    block = ForeignKeyField(column_name='block_id', field='block_id', model=CmsBlock)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore)

    class Meta:
        table_name = 'cms_block_store'
        indexes = (
            (('block', 'store'), True),
        )
        primary_key = CompositeKey('block', 'store')

class CmsPage(BaseModel):
    content = TextField(null=True)
    content_heading = CharField(null=True)
    creation_time = DateTimeField(null=True)
    custom_layout_update_xml = TextField(null=True)
    custom_root_template = CharField(null=True)
    custom_theme = CharField(null=True)
    custom_theme_from = DateField(null=True)
    custom_theme_to = DateField(null=True)
    identifier = CharField(index=True, null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")])
    layout_update_xml = TextField(null=True)
    meta_description = TextField(null=True)
    meta_keywords = TextField(null=True)
    page_id = AutoField()
    root_template = CharField(null=True)
    solr_boost = FloatField(constraints=[SQL("DEFAULT 1.0000")])
    solr_exclude = IntegerField(constraints=[SQL("DEFAULT 0")])
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    title = CharField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'cms_page'

class CmsPageStore(BaseModel):
    page = ForeignKeyField(column_name='page_id', field='page_id', model=CmsPage)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore)

    class Meta:
        table_name = 'cms_page_store'
        indexes = (
            (('page', 'store'), True),
        )
        primary_key = CompositeKey('page', 'store')

class CommercebugSnapshotNames(BaseModel):
    snapshot_name = CharField()
    snapshot_name_id = AutoField()

    class Meta:
        table_name = 'commercebug_snapshot_names'

class CommercebugSnapshots(BaseModel):
    contents = TextField(null=True)
    file = TextField(null=True)
    hash = CharField(null=True)
    snapshot_id = AutoField()
    snapshot_name_id = IntegerField()

    class Meta:
        table_name = 'commercebug_snapshots'

class CoreCache(BaseModel):
    create_time = IntegerField(null=True)
    data = TextField(null=True)
    expire_time = IntegerField(index=True, null=True)
    id = CharField(primary_key=True)
    update_time = IntegerField(null=True)

    class Meta:
        table_name = 'core_cache'

class CoreCacheOption(BaseModel):
    code = CharField(primary_key=True)
    value = IntegerField(null=True)

    class Meta:
        table_name = 'core_cache_option'

class CoreCacheTag(BaseModel):
    cache_id = CharField(index=True)
    tag = CharField()

    class Meta:
        table_name = 'core_cache_tag'
        indexes = (
            (('tag', 'cache_id'), True),
        )
        primary_key = CompositeKey('cache_id', 'tag')

class CoreConfigData(BaseModel):
    config_id = AutoField()
    path = CharField(constraints=[SQL("DEFAULT 'general'")])
    scope = CharField(constraints=[SQL("DEFAULT 'default'")])
    scope_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    value = TextField(null=True)

    class Meta:
        table_name = 'core_config_data'
        indexes = (
            (('scope', 'scope_id', 'path'), True),
        )

class CoreConfigDataDev(BaseModel):
    config_id = AutoField()
    path = CharField(constraints=[SQL("DEFAULT 'general'")])
    scope = CharField(constraints=[SQL("DEFAULT 'default'")])
    scope_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    value = TextField(null=True)

    class Meta:
        table_name = 'core_config_data_dev'
        indexes = (
            (('scope', 'scope_id', 'path'), True),
        )

class CoreEmailQueue(BaseModel):
    created_at = DateTimeField(null=True)
    entity_id = IntegerField(null=True)
    entity_type = CharField(null=True)
    event_type = CharField(null=True)
    message_body = TextField()
    message_body_hash = CharField()
    message_id = AutoField()
    message_parameters = TextField()
    processed_at = DateTimeField(null=True)

    class Meta:
        table_name = 'core_email_queue'
        indexes = (
            (('entity_id', 'entity_type', 'event_type', 'message_body_hash'), False),
        )

class CoreEmailQueueRecipients(BaseModel):
    email_type = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    message = ForeignKeyField(column_name='message_id', field='message_id', model=CoreEmailQueue)
    recipient_email = CharField(index=True)
    recipient_id = AutoField()
    recipient_name = CharField()

    class Meta:
        table_name = 'core_email_queue_recipients'
        indexes = (
            (('message', 'recipient_email', 'email_type'), True),
        )

class CoreEmailTemplate(BaseModel):
    added_at = DateTimeField(index=True, null=True)
    modified_at = DateTimeField(index=True, null=True)
    orig_template_code = CharField(null=True)
    orig_template_variables = TextField(null=True)
    template_code = CharField(unique=True)
    template_id = AutoField()
    template_sender_email = CharField(null=True)
    template_sender_name = CharField(null=True)
    template_styles = TextField(null=True)
    template_subject = CharField()
    template_text = TextField()
    template_type = IntegerField(null=True)

    class Meta:
        table_name = 'core_email_template'

class CoreFlag(BaseModel):
    flag_code = CharField()
    flag_data = TextField(null=True)
    flag_id = AutoField()
    last_update = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], index=True)
    state = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'core_flag'

class CoreLayoutUpdate(BaseModel):
    handle = CharField(index=True, null=True)
    layout_update_id = AutoField()
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    xml = TextField(null=True)

    class Meta:
        table_name = 'core_layout_update'

class CoreLayoutLink(BaseModel):
    area = CharField(null=True)
    layout_link_id = AutoField()
    layout_update = ForeignKeyField(column_name='layout_update_id', constraints=[SQL("DEFAULT 0")], field='layout_update_id', model=CoreLayoutUpdate)
    package = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    theme = CharField(null=True)

    class Meta:
        table_name = 'core_layout_link'
        indexes = (
            (('store', 'package', 'theme', 'layout_update'), True),
        )

class CoreResource(BaseModel):
    code = CharField(primary_key=True)
    data_version = CharField(null=True)
    version = CharField(null=True)

    class Meta:
        table_name = 'core_resource'

class CoreSession(BaseModel):
    session_data = TextField()
    session_expires = IntegerField(constraints=[SQL("DEFAULT 0")])
    session_id = CharField(primary_key=True)

    class Meta:
        table_name = 'core_session'

class CoreTranslate(BaseModel):
    crc_string = BigIntegerField(constraints=[SQL("DEFAULT 1591228201")])
    key_id = AutoField()
    locale = CharField(constraints=[SQL("DEFAULT 'en_US'")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    string = CharField(constraints=[SQL("DEFAULT 'Translate String'")])
    translate = CharField(null=True)

    class Meta:
        table_name = 'core_translate'
        indexes = (
            (('store', 'locale', 'crc_string', 'string'), True),
        )

class CoreUrlRewrite(BaseModel):
    category = ForeignKeyField(column_name='category_id', field='entity_id', model=CatalogCategoryEntity, null=True)
    description = CharField(null=True)
    id_path = CharField(index=True, null=True)
    is_system = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    options = CharField(null=True)
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity, null=True)
    request_path = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    target_path = CharField(null=True)
    url_rewrite_id = AutoField()

    class Meta:
        table_name = 'core_url_rewrite'
        indexes = (
            (('id_path', 'is_system', 'store'), True),
            (('request_path', 'store'), True),
            (('target_path', 'store'), False),
        )

class CoreVariable(BaseModel):
    code = CharField(null=True, unique=True)
    name = CharField(null=True)
    variable_id = AutoField()

    class Meta:
        table_name = 'core_variable'

class CoreVariableValue(BaseModel):
    html_value = TextField(null=True)
    plain_value = TextField(null=True)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value_id = AutoField()
    variable = ForeignKeyField(column_name='variable_id', constraints=[SQL("DEFAULT 0")], field='variable_id', model=CoreVariable)

    class Meta:
        table_name = 'core_variable_value'
        indexes = (
            (('variable', 'store'), True),
        )

class CouponAggregated(BaseModel):
    coupon_code = CharField(null=True)
    coupon_uses = IntegerField(constraints=[SQL("DEFAULT 0")])
    discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    discount_amount_actual = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    order_status = CharField(null=True)
    period = DateField()
    rule_name = CharField(index=True, null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    subtotal_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    subtotal_amount_actual = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_amount_actual = DecimalField(constraints=[SQL("DEFAULT 0.0000")])

    class Meta:
        table_name = 'coupon_aggregated'
        indexes = (
            (('period', 'store', 'order_status', 'coupon_code'), True),
        )

class CouponAggregatedOrder(BaseModel):
    coupon_code = CharField(null=True)
    coupon_uses = IntegerField(constraints=[SQL("DEFAULT 0")])
    discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    order_status = CharField(null=True)
    period = DateField()
    rule_name = CharField(index=True, null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    subtotal_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])

    class Meta:
        table_name = 'coupon_aggregated_order'
        indexes = (
            (('period', 'store', 'order_status', 'coupon_code'), True),
        )

class CouponAggregatedUpdated(BaseModel):
    coupon_code = CharField(null=True)
    coupon_uses = IntegerField(constraints=[SQL("DEFAULT 0")])
    discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    discount_amount_actual = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    order_status = CharField(null=True)
    period = DateField()
    rule_name = CharField(index=True, null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    subtotal_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    subtotal_amount_actual = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_amount_actual = DecimalField(constraints=[SQL("DEFAULT 0.0000")])

    class Meta:
        table_name = 'coupon_aggregated_updated'
        indexes = (
            (('period', 'store', 'order_status', 'coupon_code'), True),
        )

class CronSchedule(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    executed_at = DateTimeField(null=True)
    finished_at = DateTimeField(null=True)
    job_code = CharField(constraints=[SQL("DEFAULT '0'")], index=True)
    messages = TextField(null=True)
    schedule_id = AutoField()
    scheduled_at = DateTimeField(null=True)
    status = CharField(constraints=[SQL("DEFAULT 'pending'")])

    class Meta:
        table_name = 'cron_schedule'
        indexes = (
            (('scheduled_at', 'status'), False),
        )

class CustomerAddressEntity(BaseModel):
    attribute_set_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    entity_id = AutoField()
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    increment_id = CharField(null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")])
    parent = ForeignKeyField(column_name='parent_id', field='entity_id', model=CustomerEntity, null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])

    class Meta:
        table_name = 'customer_address_entity'

class CustomerAddressEntityDatetime(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerAddressEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    value = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    value_id = AutoField()

    class Meta:
        table_name = 'customer_address_entity_datetime'
        indexes = (
            (('entity', 'attribute'), True),
            (('entity', 'attribute', 'value'), False),
        )

class CustomerAddressEntityDecimal(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerAddressEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    value_id = AutoField()

    class Meta:
        table_name = 'customer_address_entity_decimal'
        indexes = (
            (('entity', 'attribute'), True),
            (('entity', 'attribute', 'value'), False),
        )

class CustomerAddressEntityInt(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerAddressEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    value = IntegerField(constraints=[SQL("DEFAULT 0")])
    value_id = AutoField()

    class Meta:
        table_name = 'customer_address_entity_int'
        indexes = (
            (('entity', 'attribute'), True),
            (('entity', 'attribute', 'value'), False),
        )

class CustomerAddressEntityText(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerAddressEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    value = TextField()
    value_id = AutoField()

    class Meta:
        table_name = 'customer_address_entity_text'
        indexes = (
            (('entity', 'attribute'), True),
        )

class CustomerAddressEntityVarchar(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerAddressEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    value = CharField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'customer_address_entity_varchar'
        indexes = (
            (('entity', 'attribute'), True),
            (('entity', 'attribute', 'value'), False),
        )

class CustomerEavAttribute(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', field='attribute_id', model=EavAttribute, primary_key=True)
    data_model = CharField(null=True)
    input_filter = CharField(null=True)
    is_system = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_visible = IntegerField(constraints=[SQL("DEFAULT 1")])
    multiline_count = IntegerField(constraints=[SQL("DEFAULT 1")])
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    validate_rules = TextField(null=True)

    class Meta:
        table_name = 'customer_eav_attribute'

class CustomerEavAttributeWebsite(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', field='attribute_id', model=EavAttribute)
    default_value = TextField(null=True)
    is_required = IntegerField(null=True)
    is_visible = IntegerField(null=True)
    multiline_count = IntegerField(null=True)
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'customer_eav_attribute_website'
        indexes = (
            (('attribute', 'website'), True),
        )
        primary_key = CompositeKey('attribute', 'website')

class CustomerEntityDatetime(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    value = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    value_id = AutoField()

    class Meta:
        table_name = 'customer_entity_datetime'
        indexes = (
            (('entity', 'attribute'), True),
            (('entity', 'attribute', 'value'), False),
        )

class CustomerEntityDecimal(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    value_id = AutoField()

    class Meta:
        table_name = 'customer_entity_decimal'
        indexes = (
            (('entity', 'attribute'), True),
            (('entity', 'attribute', 'value'), False),
        )

class CustomerEntityInt(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    value = IntegerField(constraints=[SQL("DEFAULT 0")])
    value_id = AutoField()

    class Meta:
        table_name = 'customer_entity_int'
        indexes = (
            (('entity', 'attribute'), True),
            (('entity', 'attribute', 'value'), False),
        )

class CustomerEntityText(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    value = TextField()
    value_id = AutoField()

    class Meta:
        table_name = 'customer_entity_text'
        indexes = (
            (('entity', 'attribute'), True),
        )

class CustomerEntityVarchar(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    value = CharField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'customer_entity_varchar'
        indexes = (
            (('entity', 'attribute'), True),
            (('entity', 'attribute', 'value'), False),
        )

class CustomerFlowpassword(BaseModel):
    email = CharField(index=True)
    flowpassword_id = AutoField()
    ip = CharField(index=True)
    requested_date = CharField(constraints=[SQL("DEFAULT '0000-00-00 00:00:00'")], index=True)

    class Meta:
        table_name = 'customer_flowpassword'

class CustomerFormAttribute(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', field='attribute_id', model=EavAttribute)
    form_code = CharField()

    class Meta:
        table_name = 'customer_form_attribute'
        indexes = (
            (('form_code', 'attribute'), True),
        )
        primary_key = CompositeKey('attribute', 'form_code')

class CustomerRelation(BaseModel):
    email = CharField(null=True)
    new_customer_id = IntegerField(null=True)
    old_customer_id = IntegerField(null=True)

    class Meta:
        table_name = 'customer_relation'

class CycleCountAuditTrail(BaseModel):
    count_correct = BooleanField(null=True)  # bit
    new_qoh = IntegerField(null=True)
    old_qoh = IntegerField(null=True)
    product_id = IntegerField(index=True, null=True)
    schedule_id = IntegerField(null=True)
    sku = CharField(null=True)
    timestamp = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    user_id = IntegerField(null=True)

    class Meta:
        table_name = 'cycle_count_audit_trail'

class CycleCountSchedule(BaseModel):
    current = BooleanField(null=True)  # bit
    name = CharField(null=True)
    schedule_id = AutoField()

    class Meta:
        table_name = 'cycle_count_schedule'

class CycleCountsUpcErrors(BaseModel):
    aisle = CharField(null=True)
    bay = CharField(null=True)
    comments = TextField(null=True)
    error_id = AutoField()
    not_in_system = UnknownField(null=True)  # bit
    product_name = CharField(null=True)
    pulled_shelf = UnknownField(null=True)  # bit
    qty_counted = IntegerField(null=True)
    shelf = CharField(null=True)
    status = IntegerField(null=True)
    timestamp = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    upc = CharField()
    updated_at = DateTimeField(null=True)
    updated_by = IntegerField(null=True)
    user_id = IntegerField(null=True)

    class Meta:
        table_name = 'cycle_counts_upc_errors'

class DataWarehouse(BaseModel):
    active_status = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    description = TextField(null=True)
    drop_ship = UnknownField(constraints=[SQL("DEFAULT b'0'")], null=True)  # bit
    ip_qty = IntegerField()
    name = CharField()
    no_barcode = UnknownField(null=True)  # bit
    order_up_to = IntegerField(constraints=[SQL("DEFAULT 0")])
    os_aisle = CharField(null=True)
    os_bay = CharField(null=True)
    os_shelf = CharField(null=True)
    plp = BooleanField()  # bit
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    product_id = IntegerField(index=True, null=True)
    reorder_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    show_description = UnknownField(null=True)  # bit
    sku = CharField(primary_key=True)
    status = IntegerField(null=True)
    upc = CharField(index=True)
    updated_at = DateTimeField(null=True)
    vendor = CharField(index=True)
    vendor_cost = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    vendor_num = CharField(index=True)
    vendor_uom = CharField()
    vendor_upc = CharField()
    no_barcode = BooleanField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'data_warehouse'

class DatafeedwatchUpdatedProducts(BaseModel):
    dfw_prod_id = AutoField()
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'datafeedwatch_updated_products'

class DataflowProfile(BaseModel):
    actions_xml = TextField(null=True)
    created_at = DateTimeField(null=True)
    data_transfer = CharField(null=True)
    direction = CharField(null=True)
    entity_type = CharField(null=True)
    gui_data = TextField(null=True)
    name = CharField(null=True)
    profile_id = AutoField()
    store_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'dataflow_profile'

class DataflowBatch(BaseModel):
    adapter = CharField(null=True)
    batch_id = AutoField()
    created_at = DateTimeField(index=True, null=True)
    params = TextField(null=True)
    profile = ForeignKeyField(column_name='profile_id', constraints=[SQL("DEFAULT 0")], field='profile_id', model=DataflowProfile)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)

    class Meta:
        table_name = 'dataflow_batch'

class DataflowBatchExport(BaseModel):
    batch_data = TextField(null=True)
    batch_export_id = BigAutoField()
    batch = ForeignKeyField(column_name='batch_id', constraints=[SQL("DEFAULT 0")], field='batch_id', model=DataflowBatch)
    status = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'dataflow_batch_export'

class DataflowBatchImport(BaseModel):
    batch_data = TextField(null=True)
    batch = ForeignKeyField(column_name='batch_id', constraints=[SQL("DEFAULT 0")], field='batch_id', model=DataflowBatch)
    batch_import_id = BigAutoField()
    status = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'dataflow_batch_import'

class DataflowSession(BaseModel):
    comment = CharField(null=True)
    created_date = DateTimeField(null=True)
    direction = CharField(null=True)
    file = CharField(null=True)
    session_id = AutoField()
    type = CharField(null=True)
    user_id = IntegerField()

    class Meta:
        table_name = 'dataflow_session'

class DataflowImportData(BaseModel):
    import_id = AutoField()
    serial_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    session = ForeignKeyField(column_name='session_id', field='session_id', model=DataflowSession, null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    value = TextField(null=True)

    class Meta:
        table_name = 'dataflow_import_data'

class DataflowProfileHistory(BaseModel):
    action_code = CharField(null=True)
    history_id = AutoField()
    performed_at = DateTimeField(null=True)
    profile = ForeignKeyField(column_name='profile_id', constraints=[SQL("DEFAULT 0")], field='profile_id', model=DataflowProfile)
    user_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'dataflow_profile_history'

class DesignChange(BaseModel):
    date_from = DateField(null=True)
    date_to = DateField(null=True)
    design = CharField(null=True)
    design_change_id = AutoField()
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)

    class Meta:
        table_name = 'design_change'

class DirectoryCountry(BaseModel):
    country_id = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    iso2_code = CharField(null=True)
    iso3_code = CharField(null=True)

    class Meta:
        table_name = 'directory_country'

class DirectoryCountryFormat(BaseModel):
    country_format_id = AutoField()
    country_id = CharField(null=True)
    format = TextField()
    type = CharField(null=True)

    class Meta:
        table_name = 'directory_country_format'
        indexes = (
            (('country_id', 'type'), True),
        )

class DirectoryCountryRegion(BaseModel):
    code = CharField(null=True)
    country_id = CharField(constraints=[SQL("DEFAULT '0'")], index=True)
    default_name = CharField(null=True)
    region_id = AutoField()

    class Meta:
        table_name = 'directory_country_region'

class DirectoryCountryRegionName(BaseModel):
    locale = CharField(constraints=[SQL("DEFAULT ''")])
    name = CharField(null=True)
    region = ForeignKeyField(column_name='region_id', constraints=[SQL("DEFAULT 0")], field='region_id', model=DirectoryCountryRegion)

    class Meta:
        table_name = 'directory_country_region_name'
        indexes = (
            (('locale', 'region'), True),
        )
        primary_key = CompositeKey('locale', 'region')

class DirectoryCurrencyRate(BaseModel):
    currency_from = CharField(constraints=[SQL("DEFAULT ''")])
    currency_to = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    rate = DecimalField(constraints=[SQL("DEFAULT 0.000000000000")])

    class Meta:
        table_name = 'directory_currency_rate'
        indexes = (
            (('currency_from', 'currency_to'), True),
        )
        primary_key = CompositeKey('currency_from', 'currency_to')

class DownloadableLink(BaseModel):
    is_shareable = IntegerField(constraints=[SQL("DEFAULT 0")])
    link_file = CharField(null=True)
    link_id = AutoField()
    link_type = CharField(null=True)
    link_url = CharField(null=True)
    number_of_downloads = IntegerField(null=True)
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    sample_file = CharField(null=True)
    sample_type = CharField(null=True)
    sample_url = CharField(null=True)
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'downloadable_link'
        indexes = (
            (('product', 'sort_order'), False),
        )

class DownloadableLinkPrice(BaseModel):
    link = ForeignKeyField(column_name='link_id', constraints=[SQL("DEFAULT 0")], field='link_id', model=DownloadableLink)
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    price_id = AutoField()
    website = ForeignKeyField(column_name='website_id', constraints=[SQL("DEFAULT 0")], field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'downloadable_link_price'

class SalesFlatOrder(BaseModel):
    adjustment_negative = DecimalField(null=True)
    adjustment_positive = DecimalField(null=True)
    applied_rule_ids = CharField(null=True)
    auctaneapi_discounts = TextField(null=True)
    base_adjustment_negative = DecimalField(null=True)
    base_adjustment_positive = DecimalField(null=True)
    base_currency_code = CharField(null=True)
    base_discount_amount = DecimalField(null=True)
    base_discount_canceled = DecimalField(null=True)
    base_discount_invoiced = DecimalField(null=True)
    base_discount_refunded = DecimalField(null=True)
    base_grand_total = DecimalField(null=True)
    base_hidden_tax_amount = DecimalField(null=True)
    base_hidden_tax_invoiced = DecimalField(null=True)
    base_hidden_tax_refunded = DecimalField(null=True)
    base_shipping_amount = DecimalField(null=True)
    base_shipping_canceled = DecimalField(null=True)
    base_shipping_discount_amount = DecimalField(null=True)
    base_shipping_hidden_tax_amnt = DecimalField(null=True)
    base_shipping_incl_tax = DecimalField(null=True)
    base_shipping_invoiced = DecimalField(null=True)
    base_shipping_refunded = DecimalField(null=True)
    base_shipping_tax_amount = DecimalField(null=True)
    base_shipping_tax_refunded = DecimalField(null=True)
    base_subtotal = DecimalField(null=True)
    base_subtotal_canceled = DecimalField(null=True)
    base_subtotal_incl_tax = DecimalField(null=True)
    base_subtotal_invoiced = DecimalField(null=True)
    base_subtotal_refunded = DecimalField(null=True)
    base_tax_amount = DecimalField(null=True)
    base_tax_canceled = DecimalField(null=True)
    base_tax_invoiced = DecimalField(null=True)
    base_tax_refunded = DecimalField(null=True)
    base_to_global_rate = DecimalField(null=True)
    base_to_order_rate = DecimalField(null=True)
    base_total_canceled = DecimalField(null=True)
    base_total_due = DecimalField(null=True)
    base_total_invoiced = DecimalField(null=True)
    base_total_invoiced_cost = DecimalField(null=True)
    base_total_offline_refunded = DecimalField(null=True)
    base_total_online_refunded = DecimalField(null=True)
    base_total_paid = DecimalField(null=True)
    base_total_qty_ordered = DecimalField(null=True)
    base_total_refunded = DecimalField(null=True)
    billing_address_id = IntegerField(null=True)
    can_ship_partially = IntegerField(null=True)
    can_ship_partially_item = IntegerField(null=True)
    comments = TextField(null=True)
    coupon_code = CharField(null=True)
    coupon_rule_name = CharField(null=True)
    created_at = DateTimeField(index=True, null=True)
    customer_dob = DateTimeField(null=True)
    customer_email = CharField(index=True, null=True)
    customer_firstname = CharField(null=True)
    customer_gender = IntegerField(null=True)
    customer_group_id = IntegerField(null=True)
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity, null=True)
    customer_is_guest = IntegerField(null=True)
    customer_lastname = CharField(null=True)
    customer_middlename = CharField(null=True)
    customer_note = TextField(null=True)
    customer_note_notify = IntegerField(null=True)
    customer_prefix = CharField(null=True)
    customer_suffix = CharField(null=True)
    customer_taxvat = CharField(null=True)
    discount_amount = DecimalField(null=True)
    discount_canceled = DecimalField(null=True)
    discount_description = CharField(null=True)
    discount_invoiced = DecimalField(null=True)
    discount_refunded = DecimalField(null=True)
    ebizmarts_abandonedcart_flag = IntegerField(null=True)
    ebizmarts_magemonkey_campaign_id = CharField(null=True)
    edit_increment = IntegerField(null=True)
    email_sent = IntegerField(null=True)
    entity_id = AutoField()
    ext_customer_id = CharField(null=True)
    ext_order_id = CharField(index=True, null=True)
    forced_shipment_with_invoice = IntegerField(null=True)
    gift_message_id = IntegerField(null=True)
    global_currency_code = CharField(null=True)
    grand_total = DecimalField(null=True)
    hidden_tax_amount = DecimalField(null=True)
    hidden_tax_invoiced = DecimalField(null=True)
    hidden_tax_refunded = DecimalField(null=True)
    hold_before_state = CharField(null=True)
    hold_before_status = CharField(null=True)
    increment_id = CharField(null=True, unique=True)
    is_virtual = IntegerField(null=True)
    mailchimp_abandonedcart_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    mailchimp_campaign_id = CharField(null=True)
    mailchimp_landing_page = CharField(constraints=[SQL("DEFAULT ''")])
    onestepcheckout_giftwrap_amount = DecimalField(null=True)
    onestepcheckout_order_comment = TextField(null=True)
    order_currency_code = CharField(null=True)
    original_increment_id = CharField(null=True)
    party_date = DateTimeField(null=True)
    payment_auth_expiration = IntegerField(null=True)
    payment_authorization_amount = DecimalField(null=True)
    paypal_ipn_customer_notified = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    protect_code = CharField(null=True)
    quote_address_id = IntegerField(null=True)
    quote_id = IntegerField(index=True, null=True)
    relation_child_id = CharField(null=True)
    relation_child_real_id = CharField(null=True)
    relation_parent_id = CharField(null=True)
    relation_parent_real_id = CharField(null=True)
    remote_ip = CharField(null=True)
    rjm_utm_campaign = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    rjm_utm_content = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    rjm_utm_medium = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    rjm_utm_source = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    rjm_utm_term = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    shipping_address_id = IntegerField(null=True)
    shipping_amount = DecimalField(null=True)
    shipping_canceled = DecimalField(null=True)
    shipping_description = CharField(null=True)
    shipping_discount_amount = DecimalField(null=True)
    shipping_hidden_tax_amount = DecimalField(null=True)
    shipping_incl_tax = DecimalField(null=True)
    shipping_invoiced = DecimalField(null=True)
    shipping_method = CharField(null=True)
    shipping_pobox = IntegerField(null=True)
    shipping_refunded = DecimalField(null=True)
    shipping_tax_amount = DecimalField(null=True)
    shipping_tax_refunded = DecimalField(null=True)
    state = CharField(index=True, null=True)
    status = CharField(index=True, null=True)
    store_currency_code = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    store_name = CharField(null=True)
    store_to_base_rate = DecimalField(null=True)
    store_to_order_rate = DecimalField(null=True)
    subtotal = DecimalField(null=True)
    subtotal_canceled = DecimalField(null=True)
    subtotal_incl_tax = DecimalField(null=True)
    subtotal_invoiced = DecimalField(null=True)
    subtotal_refunded = DecimalField(null=True)
    tax_amount = DecimalField(null=True)
    tax_canceled = DecimalField(null=True)
    tax_invoiced = DecimalField(null=True)
    tax_refunded = DecimalField(null=True)
    total_canceled = DecimalField(null=True)
    total_due = DecimalField(null=True)
    total_invoiced = DecimalField(null=True)
    total_item_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    total_offline_refunded = DecimalField(null=True)
    total_online_refunded = DecimalField(null=True)
    total_paid = DecimalField(null=True)
    total_qty_ordered = DecimalField(null=True)
    total_refunded = DecimalField(null=True)
    updated_at = DateTimeField(index=True, null=True)
    weight = DecimalField(null=True)
    x_forwarded_for = CharField(null=True)

    class Meta:
        table_name = 'sales_flat_order'
        indexes = (
            (('created_at', 'increment_id', 'entity_id'), True),
        )

class DownloadableLinkPurchased(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    customer = ForeignKeyField(column_name='customer_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerEntity, null=True)
    link_section_title = CharField(null=True)
    order = ForeignKeyField(column_name='order_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=SalesFlatOrder, null=True)
    order_increment_id = CharField(null=True)
    order_item_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    product_name = CharField(null=True)
    product_sku = CharField(null=True)
    purchased_id = AutoField()
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])

    class Meta:
        table_name = 'downloadable_link_purchased'

class SalesFlatOrderItem(BaseModel):
    additional_data = TextField(null=True)
    amount_refunded = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    applied_rule_ids = TextField(null=True)
    base_amount_refunded = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    base_cost = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    base_discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    base_discount_invoiced = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    base_discount_refunded = DecimalField(null=True)
    base_hidden_tax_amount = DecimalField(null=True)
    base_hidden_tax_invoiced = DecimalField(null=True)
    base_hidden_tax_refunded = DecimalField(null=True)
    base_original_price = DecimalField(null=True)
    base_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    base_price_incl_tax = DecimalField(null=True)
    base_row_invoiced = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    base_row_total = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    base_row_total_incl_tax = DecimalField(null=True)
    base_tax_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    base_tax_before_discount = DecimalField(null=True)
    base_tax_invoiced = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    base_tax_refunded = DecimalField(null=True)
    base_weee_tax_applied_amount = DecimalField(null=True)
    base_weee_tax_applied_row_amnt = DecimalField(null=True)
    base_weee_tax_disposition = DecimalField(null=True)
    base_weee_tax_row_disposition = DecimalField(null=True)
    category_cart_add = IntegerField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    description = TextField(null=True)
    discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    discount_invoiced = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    discount_percent = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    discount_refunded = DecimalField(null=True)
    ext_order_item_id = CharField(null=True)
    free_shipping = IntegerField(constraints=[SQL("DEFAULT 0")])
    gift_message_available = IntegerField(null=True)
    gift_message_id = IntegerField(null=True)
    hidden_tax_amount = DecimalField(null=True)
    hidden_tax_canceled = DecimalField(null=True)
    hidden_tax_invoiced = DecimalField(null=True)
    hidden_tax_refunded = DecimalField(null=True)
    is_nominal = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_qty_decimal = IntegerField(null=True)
    is_virtual = IntegerField(null=True)
    item_id = AutoField()
    locked_do_invoice = IntegerField(null=True)
    locked_do_ship = IntegerField(null=True)
    name = CharField(null=True)
    no_discount = IntegerField(constraints=[SQL("DEFAULT 0")])
    order_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    original_price = DecimalField(null=True)
    parent_item_id = IntegerField(null=True)
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    price_incl_tax = DecimalField(null=True)
    product_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    product_options = TextField(null=True)
    product_type = CharField(null=True)
    qty_backordered = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    qty_canceled = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    qty_invoiced = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    qty_ordered = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    qty_refunded = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    qty_shipped = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    quote_item_id = IntegerField(null=True)
    row_invoiced = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    row_total = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    row_total_incl_tax = DecimalField(null=True)
    row_weight = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    sku = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    tax_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    tax_before_discount = DecimalField(null=True)
    tax_canceled = DecimalField(null=True)
    tax_invoiced = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    tax_percent = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    tax_refunded = DecimalField(null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    weee_tax_applied = TextField(null=True)
    weee_tax_applied_amount = DecimalField(null=True)
    weee_tax_applied_row_amount = DecimalField(null=True)
    weee_tax_disposition = DecimalField(null=True)
    weee_tax_row_disposition = DecimalField(null=True)
    weight = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)

    class Meta:
        table_name = 'sales_flat_order_item'
        indexes = (
            (('sku', 'created_at', 'qty_ordered'), False),
            (('sku', 'created_at', 'qty_shipped'), False),
        )

class DownloadableLinkPurchasedItem(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    is_shareable = IntegerField(constraints=[SQL("DEFAULT 0")])
    item_id = AutoField()
    link_file = CharField(null=True)
    link_hash = CharField(index=True, null=True)
    link_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    link_title = CharField(null=True)
    link_type = CharField(null=True)
    link_url = CharField(null=True)
    number_of_downloads_bought = IntegerField(constraints=[SQL("DEFAULT 0")])
    number_of_downloads_used = IntegerField(constraints=[SQL("DEFAULT 0")])
    order_item = ForeignKeyField(column_name='order_item_id', constraints=[SQL("DEFAULT 0")], field='item_id', model=SalesFlatOrderItem, null=True)
    product_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    purchased = ForeignKeyField(column_name='purchased_id', constraints=[SQL("DEFAULT 0")], field='purchased_id', model=DownloadableLinkPurchased)
    status = CharField(null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])

    class Meta:
        table_name = 'downloadable_link_purchased_item'

class DownloadableLinkTitle(BaseModel):
    link = ForeignKeyField(column_name='link_id', constraints=[SQL("DEFAULT 0")], field='link_id', model=DownloadableLink)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    title = CharField(null=True)
    title_id = AutoField()

    class Meta:
        table_name = 'downloadable_link_title'
        indexes = (
            (('link', 'store'), True),
        )

class DownloadableSample(BaseModel):
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    sample_file = CharField(null=True)
    sample_id = AutoField()
    sample_type = CharField(null=True)
    sample_url = CharField(null=True)
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'downloadable_sample'

class DownloadableSampleTitle(BaseModel):
    sample = ForeignKeyField(column_name='sample_id', constraints=[SQL("DEFAULT 0")], field='sample_id', model=DownloadableSample)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    title = CharField(null=True)
    title_id = AutoField()

    class Meta:
        table_name = 'downloadable_sample_title'
        indexes = (
            (('sample', 'store'), True),
        )

class DpsUrlRewritePrefer(BaseModel):
    product_id = IntegerField(null=True)
    url_rewrite_id = IntegerField(null=True)

    class Meta:
        table_name = 'dps_url_rewrite_prefer'

class EavAttributeGroup(BaseModel):
    attribute_group_id = AutoField()
    attribute_group_name = CharField(null=True)
    attribute_set = ForeignKeyField(column_name='attribute_set_id', constraints=[SQL("DEFAULT 0")], field='attribute_set_id', model=EavAttributeSet)
    default_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'eav_attribute_group'
        indexes = (
            (('attribute_set', 'attribute_group_name'), True),
            (('attribute_set', 'sort_order'), False),
        )

class EavAttributeLabel(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    attribute_label_id = AutoField()
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = CharField(null=True)

    class Meta:
        table_name = 'eav_attribute_label'
        indexes = (
            (('attribute', 'store'), False),
        )

class EavAttributeOption(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    option_id = AutoField()
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'eav_attribute_option'

class EavAttributeOptionValue(BaseModel):
    option = ForeignKeyField(column_name='option_id', constraints=[SQL("DEFAULT 0")], field='option_id', model=EavAttributeOption)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = CharField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'eav_attribute_option_value'

class EavEntity(BaseModel):
    attribute_set_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    entity_id = AutoField()
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    increment_id = CharField(null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")])
    parent_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])

    class Meta:
        table_name = 'eav_entity'

class EavEntityAttribute(BaseModel):
    attribute_group = ForeignKeyField(column_name='attribute_group_id', constraints=[SQL("DEFAULT 0")], field='attribute_group_id', model=EavAttributeGroup)
    attribute = ForeignKeyField(column_name='attribute_id', constraints=[SQL("DEFAULT 0")], field='attribute_id', model=EavAttribute)
    attribute_set_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    entity_attribute_id = AutoField()
    entity_type_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'eav_entity_attribute'
        indexes = (
            (('attribute_group', 'attribute'), True),
            (('attribute_set_id', 'attribute'), True),
            (('attribute_set_id', 'sort_order'), False),
        )

class EavEntityDatetime(BaseModel):
    attribute_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=EavEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    value_id = AutoField()

    class Meta:
        table_name = 'eav_entity_datetime'
        indexes = (
            (('attribute_id', 'value'), False),
            (('entity', 'attribute_id', 'store'), True),
            (('entity_type', 'value'), False),
        )

class EavEntityDecimal(BaseModel):
    attribute_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=EavEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    value_id = AutoField()

    class Meta:
        table_name = 'eav_entity_decimal'
        indexes = (
            (('attribute_id', 'value'), False),
            (('entity', 'attribute_id', 'store'), True),
            (('entity_type', 'value'), False),
        )

class EavEntityInt(BaseModel):
    attribute_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=EavEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = IntegerField(constraints=[SQL("DEFAULT 0")])
    value_id = AutoField()

    class Meta:
        table_name = 'eav_entity_int'
        indexes = (
            (('attribute_id', 'value'), False),
            (('entity', 'attribute_id', 'store'), True),
            (('entity_type', 'value'), False),
        )

class EavEntityStore(BaseModel):
    entity_store_id = AutoField()
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    increment_last_id = CharField(null=True)
    increment_prefix = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)

    class Meta:
        table_name = 'eav_entity_store'

class EavEntityText(BaseModel):
    attribute_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=EavEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = TextField()
    value_id = AutoField()

    class Meta:
        table_name = 'eav_entity_text'
        indexes = (
            (('entity', 'attribute_id', 'store'), True),
        )

class EavEntityVarchar(BaseModel):
    attribute_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=EavEntity)
    entity_type = ForeignKeyField(column_name='entity_type_id', constraints=[SQL("DEFAULT 0")], field='entity_type_id', model=EavEntityType)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = CharField(null=True)
    value_id = AutoField()

    class Meta:
        table_name = 'eav_entity_varchar'
        indexes = (
            (('attribute_id', 'value'), False),
            (('entity', 'attribute_id', 'store'), True),
            (('entity_type', 'value'), False),
        )

class EavFormType(BaseModel):
    code = CharField()
    is_system = IntegerField(constraints=[SQL("DEFAULT 0")])
    label = CharField()
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore)
    theme = CharField(null=True)
    type_id = AutoField()

    class Meta:
        table_name = 'eav_form_type'
        indexes = (
            (('code', 'theme', 'store'), True),
        )

class EavFormFieldset(BaseModel):
    code = CharField()
    fieldset_id = AutoField()
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = ForeignKeyField(column_name='type_id', field='type_id', model=EavFormType)

    class Meta:
        table_name = 'eav_form_fieldset'
        indexes = (
            (('type', 'code'), True),
        )

class EavFormElement(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', field='attribute_id', model=EavAttribute)
    element_id = AutoField()
    fieldset = ForeignKeyField(column_name='fieldset_id', field='fieldset_id', model=EavFormFieldset, null=True)
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = ForeignKeyField(column_name='type_id', field='type_id', model=EavFormType)

    class Meta:
        table_name = 'eav_form_element'
        indexes = (
            (('type', 'attribute'), True),
        )

class EavFormFieldsetLabel(BaseModel):
    fieldset = ForeignKeyField(column_name='fieldset_id', field='fieldset_id', model=EavFormFieldset)
    label = CharField()
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore)

    class Meta:
        table_name = 'eav_form_fieldset_label'
        indexes = (
            (('fieldset', 'store'), True),
        )
        primary_key = CompositeKey('fieldset', 'store')

class EavFormTypeEntity(BaseModel):
    entity_type = ForeignKeyField(column_name='entity_type_id', field='entity_type_id', model=EavEntityType)
    type = ForeignKeyField(column_name='type_id', field='type_id', model=EavFormType)

    class Meta:
        table_name = 'eav_form_type_entity'
        indexes = (
            (('type', 'entity_type'), True),
        )
        primary_key = CompositeKey('entity_type', 'type')

class EbizmartsAbandonedcartAbtesting(BaseModel):
    current_status = IntegerField(null=True)
    store_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'ebizmarts_abandonedcart_abtesting'

class EbizmartsAbandonedcartPopup(BaseModel):
    counter = IntegerField(null=True)
    email = CharField(null=True)
    processed = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    store_id = IntegerField(null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'ebizmarts_abandonedcart_popup'

class EbizmartsAutoresponderBacktostock(BaseModel):
    alert_id = IntegerField(null=True)
    backtostock_id = AutoField()
    email = CharField(null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")])
    store_id = IntegerField(null=True)

    class Meta:
        table_name = 'ebizmarts_autoresponder_backtostock'

class EbizmartsAutoresponderBacktostockAlert(BaseModel):
    alert_id = AutoField()
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")])
    product_id = IntegerField(null=True)

    class Meta:
        table_name = 'ebizmarts_autoresponder_backtostock_alert'

class EbizmartsAutoresponderReview(BaseModel):
    counter = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    customer_id = IntegerField(null=True)
    items = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    order_id = IntegerField()
    store_id = IntegerField(null=True)
    token = CharField(null=True)

    class Meta:
        table_name = 'ebizmarts_autoresponder_review'

class EbizmartsAutoresponderUnsubscribe(BaseModel):
    email = CharField(null=True)
    list = CharField(null=True)
    store_id = IntegerField(null=True)
    unsubscribed_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'ebizmarts_autoresponder_unsubscribe'

class EbizmartsAutoresponderVisited(BaseModel):
    customer_email = CharField(null=True)
    customer_id = IntegerField(null=True)
    product_id = IntegerField(null=True)
    store_id = IntegerField(null=True)
    visited_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'ebizmarts_autoresponder_visited'

class Firstdatagge4(BaseModel):
    authorization_num = CharField()
    bank_response_code = CharField()
    bank_response_msg = CharField()
    client_ip = CharField()
    ctr = TextField()
    id = BigAutoField()
    order_id = BigIntegerField()
    transaction_tag = CharField()
    transaction_type = CharField()

    class Meta:
        table_name = 'firstdatagge4'

class GiftMessage(BaseModel):
    customer_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    gift_message_id = AutoField()
    message = TextField(null=True)
    recipient = CharField(null=True)
    sender = CharField(null=True)

    class Meta:
        table_name = 'gift_message'

class ImportexportImportdata(BaseModel):
    behavior = CharField(constraints=[SQL("DEFAULT 'append'")])
    data = TextField(null=True)
    entity = CharField()

    class Meta:
        table_name = 'importexport_importdata'

class IndexEvent(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    entity = CharField()
    entity_pk = BigIntegerField(null=True)
    event_id = BigAutoField()
    new_data = TextField(null=True)
    old_data = TextField(null=True)
    type = CharField()

    class Meta:
        table_name = 'index_event'
        indexes = (
            (('type', 'entity', 'entity_pk'), True),
        )

class IndexProcess(BaseModel):
    ended_at = DateTimeField(null=True)
    indexer_code = CharField(unique=True)
    mode = CharField(constraints=[SQL("DEFAULT 'real_time'")])
    process_id = AutoField()
    started_at = DateTimeField(null=True)
    status = CharField(constraints=[SQL("DEFAULT 'pending'")])

    class Meta:
        table_name = 'index_process'

class IndexProcessEvent(BaseModel):
    event = ForeignKeyField(column_name='event_id', field='event_id', model=IndexEvent)
    process = ForeignKeyField(column_name='process_id', field='process_id', model=IndexProcess)
    status = CharField(constraints=[SQL("DEFAULT 'new'")])

    class Meta:
        table_name = 'index_process_event'
        indexes = (
            (('process', 'event'), True),
        )
        primary_key = CompositeKey('event', 'process')

class InventoryOos(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    date_oos_end = DateTimeField(null=True)
    date_oos_start = DateTimeField(null=True)
    oos_id = AutoField()
    product_id = IntegerField(null=True)
    sku = CharField(null=True)

    class Meta:
        table_name = 'inventory_oos'

class IwdNotification(BaseModel):
    date_added = DateTimeField()
    description = TextField()
    entity_id = AutoField()
    out_id = IntegerField(null=True)
    severity = IntegerField(null=True)
    title = TextField(null=True)
    url = TextField(null=True)
    view = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'iwd_notification'

class KlaviyoReclaimCheckout(BaseModel):
    checkout_id = CharField()
    quote_id = IntegerField(index=True)

    class Meta:
        table_name = 'klaviyo_reclaim_checkout'
        indexes = (
            (('checkout_id', 'quote_id'), True),
        )
        primary_key = CompositeKey('checkout_id', 'quote_id')

class ListrakRemarketingClick(BaseModel):
    click_date = DateTimeField()
    click_id = AutoField()
    querystring = CharField()
    session_id = IntegerField(index=True)
    token_uid = CharField()

    class Meta:
        table_name = 'listrak_remarketing_click'

class ListrakRemarketingEmailcapture(BaseModel):
    emailcapture_id = AutoField()
    field_id = CharField()
    page = CharField()

    class Meta:
        table_name = 'listrak_remarketing_emailcapture'

class ListrakRemarketingLog(BaseModel):
    date_entered = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    log_type_id = IntegerField(index=True)
    message = TextField()
    store_id = IntegerField(null=True)

    class Meta:
        table_name = 'listrak_remarketing_log'

class ListrakRemarketingProductAttributeSetMap(BaseModel):
    attribute_set_id = IntegerField(index=True)
    brand_attribute_code = CharField(null=True)
    categories_source = CharField(null=True)
    category_attribute_code = CharField(null=True)
    map_id = AutoField()
    subcategory_attribute_code = CharField(null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    use_config_categories_source = IntegerField(constraints=[SQL("DEFAULT 1")])

    class Meta:
        table_name = 'listrak_remarketing_product_attribute_set_map'

class ListrakRemarketingReviewUpdate(BaseModel):
    activity = IntegerField()
    activity_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    entity_id = IntegerField()
    entity_pk_value = BigIntegerField()
    review_id = BigIntegerField()
    update_id = AutoField()

    class Meta:
        table_name = 'listrak_remarketing_review_update'

class ListrakRemarketingSession(BaseModel):
    created_at = DateTimeField(null=True)
    customer_id = IntegerField(null=True)
    had_items = IntegerField(constraints=[SQL("DEFAULT 0")])
    ips = CharField(null=True)
    pi_id = CharField(null=True)
    quote_id = IntegerField(index=True, null=True)
    session_id = CharField(unique=True)
    store_id = IntegerField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'listrak_remarketing_session'

class ListrakRemarketingSessionEmail(BaseModel):
    created_at = DateTimeField()
    email = CharField()
    emailcapture_id = IntegerField(null=True)
    session_id = IntegerField(index=True)
    type = CharField()

    class Meta:
        table_name = 'listrak_remarketing_session_email'

class ListrakRemarketingSubscriberUpdate(BaseModel):
    subscriber_id = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'listrak_remarketing_subscriber_update'

class LogCustomer(BaseModel):
    customer_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    log_id = AutoField()
    login_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    logout_at = DateTimeField(null=True)
    store_id = IntegerField()
    visitor_id = BigIntegerField(index=True, null=True)

    class Meta:
        table_name = 'log_customer'

class LogQuote(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    deleted_at = DateTimeField(null=True)
    quote_id = AutoField()
    visitor_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'log_quote'

class LogSummary(BaseModel):
    add_date = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    customer_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    store_id = IntegerField()
    summary_id = BigAutoField()
    type_id = IntegerField(null=True)
    visitor_count = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'log_summary'

class LogSummaryType(BaseModel):
    period = IntegerField(constraints=[SQL("DEFAULT 0")])
    period_type = CharField(constraints=[SQL("DEFAULT 'MINUTE'")])
    type_code = CharField(null=True)
    type_id = AutoField()

    class Meta:
        table_name = 'log_summary_type'

class LogUrl(BaseModel):
    url_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    visit_time = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    visitor_id = BigIntegerField(index=True, null=True)

    class Meta:
        table_name = 'log_url'
        primary_key = False

class LogUrlInfo(BaseModel):
    referer = CharField(null=True)
    url = CharField(null=True)
    url_id = BigAutoField()

    class Meta:
        table_name = 'log_url_info'

class LogVisitor(BaseModel):
    first_visit_at = DateTimeField(null=True)
    last_url_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    last_visit_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    session_id = CharField(null=True)
    store_id = IntegerField()
    visitor_id = BigAutoField()

    class Meta:
        table_name = 'log_visitor'

class LogVisitorInfo(BaseModel):
    http_accept_charset = CharField(null=True)
    http_accept_language = CharField(null=True)
    http_referer = CharField(null=True)
    http_user_agent = CharField(null=True)
    remote_addr = CharField(null=True)
    server_addr = CharField(null=True)
    visitor_id = BigAutoField()

    class Meta:
        table_name = 'log_visitor_info'

class LogVisitorOnline(BaseModel):
    customer_id = IntegerField(index=True, null=True)
    first_visit_at = DateTimeField(null=True)
    last_url = CharField(null=True)
    last_visit_at = DateTimeField(null=True)
    remote_addr = CharField(null=True)
    visitor_id = BigAutoField()
    visitor_type = CharField(index=True)

    class Meta:
        table_name = 'log_visitor_online'
        indexes = (
            (('first_visit_at', 'last_visit_at'), False),
        )

class M2EproBackupV611EbayOrder(BaseModel):
    best_offer = IntegerField(constraints=[SQL("DEFAULT 0")])
    buyer_email = CharField(index=True)
    buyer_name = CharField(index=True)
    buyer_user_id = CharField(index=True)
    checkout_buyer_message = CharField(null=True)
    checkout_status = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    currency = CharField()
    ebay_order_id = CharField(index=True)
    final_fee = DecimalField()
    get_it_fast = IntegerField(constraints=[SQL("DEFAULT 0")])
    global_shipping_details = TextField(null=True)
    order_id = AutoField()
    paid_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], index=True)
    payment_date = DateTimeField(null=True)
    payment_method = CharField(null=True)
    payment_status = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    payment_status_ebay = CharField(null=True)
    payment_status_hold = CharField(null=True)
    purchase_create_date = DateTimeField(null=True)
    purchase_update_date = DateTimeField(null=True)
    saved_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    selling_manager_record_number = IntegerField(index=True, null=True)
    shipping_address = TextField()
    shipping_date = DateTimeField(null=True)
    shipping_method = CharField(null=True)
    shipping_method_selected = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipping_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    shipping_status = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    shipping_tracking_details = CharField(null=True)
    shipping_type = CharField(null=True)
    tax_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    tax_includes_shipping = IntegerField(constraints=[SQL("DEFAULT 0")])
    tax_rate = FloatField(constraints=[SQL("DEFAULT 0")])
    tax_state = CharField(null=True)

    class Meta:
        table_name = 'm2epro__backup_v611_ebay_order'

class M2EproBackupV611EbayOrderItem(BaseModel):
    auto_pay = IntegerField(constraints=[SQL("DEFAULT 0")])
    buy_it_now_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    condition_display_name = CharField(null=True)
    currency = CharField()
    item_id = DecimalField(index=True)
    listing_type = CharField()
    order_item_id = AutoField()
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    qty_purchased = IntegerField()
    sku = CharField(index=True, null=True)
    title = CharField(index=True)
    transaction_id = CharField(index=True)
    unpaid_item_process_state = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    variation = TextField(null=True)

    class Meta:
        table_name = 'm2epro__backup_v611_ebay_order_item'

class M2EproAccount(BaseModel):
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    title = CharField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_account'

class M2EproAmazonAccount(BaseModel):
    account_id = AutoField()
    info = TextField(null=True)
    magento_orders_settings = TextField()
    marketplace_id = IntegerField()
    merchant_id = CharField()
    orders_last_synchronization = DateTimeField(null=True)
    other_listings_mapping_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    other_listings_mapping_settings = CharField(null=True)
    other_listings_move_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    other_listings_move_settings = CharField(null=True)
    other_listings_synchronization = IntegerField(constraints=[SQL("DEFAULT 1")])
    related_store_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    repricing = TextField(null=True)
    server_hash = CharField()
    token = CharField(null=True)

    class Meta:
        table_name = 'm2epro_amazon_account'

class M2EproAmazonDictionaryCategory(BaseModel):
    browsenode_id = DecimalField(index=True)
    category_id = IntegerField(index=True)
    is_leaf = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    keywords = TextField(null=True)
    marketplace_id = IntegerField(index=True)
    parent_category_id = IntegerField(index=True, null=True)
    path = CharField(index=True, null=True)
    product_data_nicks = CharField(index=True, null=True)
    title = CharField(index=True)

    class Meta:
        table_name = 'm2epro_amazon_dictionary_category'

class M2EproAmazonDictionaryCategoryProductData(BaseModel):
    browsenode_id = IntegerField(index=True)
    is_applicable = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    marketplace_id = IntegerField(index=True)
    product_data_nick = CharField(index=True)
    required_attributes = TextField(null=True)

    class Meta:
        table_name = 'm2epro_amazon_dictionary_category_product_data'

class M2EproAmazonDictionaryMarketplace(BaseModel):
    client_details_last_update_date = DateTimeField(null=True)
    marketplace_id = IntegerField(index=True)
    product_data = TextField(null=True)
    server_details_last_update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_amazon_dictionary_marketplace'

class M2EproAmazonDictionaryShippingOverride(BaseModel):
    location = CharField()
    marketplace_id = IntegerField(index=True)
    option = CharField()
    service = CharField()

    class Meta:
        table_name = 'm2epro_amazon_dictionary_shipping_override'

class M2EproAmazonDictionarySpecific(BaseModel):
    data_definition = TextField(null=True)
    marketplace_id = IntegerField(index=True)
    max_occurs = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    min_occurs = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    params = TextField(null=True)
    parent_specific_id = IntegerField(index=True, null=True)
    product_data_nick = CharField(index=True)
    recommended_values = TextField(null=True)
    specific_id = IntegerField(index=True)
    title = CharField(index=True)
    type = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    values = TextField(null=True)
    xml_tag = CharField(index=True)
    xpath = CharField(index=True)

    class Meta:
        table_name = 'm2epro_amazon_dictionary_specific'

class M2EproAmazonItem(BaseModel):
    account_id = IntegerField(index=True)
    create_date = DateTimeField(null=True)
    marketplace_id = IntegerField(index=True)
    product_id = IntegerField(index=True)
    sku = CharField(index=True)
    store_id = IntegerField(index=True)
    update_date = DateTimeField(null=True)
    variation_channel_options = TextField(null=True)
    variation_product_options = TextField(null=True)

    class Meta:
        table_name = 'm2epro_amazon_item'

class M2EproAmazonListing(BaseModel):
    auto_global_adding_description_template_id = IntegerField(index=True, null=True)
    auto_website_adding_description_template_id = IntegerField(index=True, null=True)
    condition_custom_attribute = CharField()
    condition_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    condition_note_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    condition_note_value = CharField()
    condition_value = CharField()
    gallery_images_attribute = CharField()
    gallery_images_limit = IntegerField(constraints=[SQL("DEFAULT 1")])
    gallery_images_mode = IntegerField()
    general_id_custom_attribute = CharField()
    general_id_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    generate_sku_mode = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    gift_message_attribute = CharField()
    gift_message_mode = IntegerField()
    gift_wrap_attribute = CharField()
    gift_wrap_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    handling_time_custom_attribute = CharField()
    handling_time_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    handling_time_value = IntegerField(constraints=[SQL("DEFAULT 1")])
    image_main_attribute = CharField()
    image_main_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    listing_id = AutoField()
    restock_date_custom_attribute = CharField()
    restock_date_mode = IntegerField(constraints=[SQL("DEFAULT 1")])
    restock_date_value = DateTimeField()
    search_by_magento_title_mode = IntegerField(constraints=[SQL("DEFAULT 1")])
    sku_custom_attribute = CharField()
    sku_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    sku_modification_custom_value = CharField()
    sku_modification_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    template_selling_format_id = IntegerField(index=True)
    template_synchronization_id = IntegerField(index=True)
    worldwide_id_custom_attribute = CharField()
    worldwide_id_mode = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'm2epro_amazon_listing'

class M2EproAmazonListingAutoCategoryGroup(BaseModel):
    adding_description_template_id = IntegerField(index=True, null=True)
    listing_auto_category_group_id = AutoField()

    class Meta:
        table_name = 'm2epro_amazon_listing_auto_category_group'

class M2EproAmazonListingOther(BaseModel):
    general_id = CharField(index=True)
    is_afn_channel = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_isbn_general_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_repricing = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    listing_other_id = AutoField()
    online_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")], index=True)
    online_qty = IntegerField(index=True, null=True)
    sku = CharField(index=True)
    title = CharField(index=True, null=True)

    class Meta:
        table_name = 'm2epro_amazon_listing_other'

class M2EproAmazonListingProduct(BaseModel):
    defected_messages = TextField(null=True)
    general_id = CharField(index=True, null=True)
    general_id_search_info = TextField(null=True)
    is_afn_channel = IntegerField(index=True, null=True)
    is_general_id_owner = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_isbn_general_id = IntegerField(index=True, null=True)
    is_repricing = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_variation_channel_matched = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_variation_parent = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_variation_product = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_variation_product_matched = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    listing_product_id = AutoField()
    online_price = DecimalField(index=True, null=True)
    online_qty = IntegerField(index=True, null=True)
    online_sale_price = DecimalField(index=True, null=True)
    online_sale_price_end_date = DateTimeField(null=True)
    online_sale_price_start_date = DateTimeField(null=True)
    search_settings_data = TextField(null=True)
    search_settings_status = IntegerField(index=True, null=True)
    sku = CharField(index=True, null=True)
    template_description_id = IntegerField(index=True, null=True)
    template_shipping_override_id = IntegerField(index=True, null=True)
    variation_child_statuses = TextField(null=True)
    variation_parent_id = IntegerField(index=True, null=True)
    variation_parent_need_processor = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'm2epro_amazon_listing_product'

class M2EproAmazonListingProductVariation(BaseModel):
    listing_product_variation_id = AutoField()

    class Meta:
        table_name = 'm2epro_amazon_listing_product_variation'

class M2EproAmazonListingProductVariationOption(BaseModel):
    listing_product_variation_option_id = AutoField()

    class Meta:
        table_name = 'm2epro_amazon_listing_product_variation_option'

class M2EproAmazonMarketplace(BaseModel):
    default_currency = CharField()
    developer_key = CharField(null=True)
    is_asin_available = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    is_merchant_fulfillment_available = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    marketplace_id = AutoField()

    class Meta:
        table_name = 'm2epro_amazon_marketplace'

class M2EproAmazonOrder(BaseModel):
    amazon_order_id = CharField(index=True)
    buyer_email = CharField(index=True, null=True)
    buyer_name = CharField(index=True)
    currency = CharField()
    discount_details = TextField(null=True)
    is_afn_channel = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_prime = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    merchant_fulfillment_data = TextField(null=True)
    merchant_fulfillment_label = TextField(null=True)
    order_id = AutoField()
    paid_amount = DecimalField(index=True)
    purchase_create_date = DateTimeField(null=True)
    purchase_update_date = DateTimeField(null=True)
    qty_shipped = IntegerField(constraints=[SQL("DEFAULT 0")])
    qty_unshipped = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipping_address = TextField()
    shipping_dates = TextField(null=True)
    shipping_price = DecimalField()
    shipping_service = CharField(null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    tax_details = TextField(null=True)

    class Meta:
        table_name = 'm2epro_amazon_order'

class M2EproAmazonOrderItem(BaseModel):
    amazon_order_item_id = CharField()
    currency = CharField()
    discount_details = TextField(null=True)
    general_id = CharField(index=True, null=True)
    gift_message = CharField(null=True)
    gift_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    gift_type = CharField(null=True)
    is_isbn_general_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    order_item_id = AutoField()
    price = DecimalField()
    qty_purchased = IntegerField(constraints=[SQL("DEFAULT 0")])
    sku = CharField(index=True, null=True)
    tax_details = TextField(null=True)
    title = CharField(index=True)

    class Meta:
        table_name = 'm2epro_amazon_order_item'

class M2EproAmazonProcessedInventory(BaseModel):
    hash = CharField(index=True)
    sku = CharField(index=True)

    class Meta:
        table_name = 'm2epro_amazon_processed_inventory'
        primary_key = False

class M2EproAmazonTemplateDescription(BaseModel):
    browsenode_id = DecimalField(index=True, null=True)
    category_path = CharField(null=True)
    is_new_asin_accepted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True, null=True)
    marketplace_id = IntegerField(index=True)
    product_data_nick = CharField(index=True, null=True)
    registered_parameter = CharField(null=True)
    template_description_id = AutoField()
    worldwide_id_custom_attribute = CharField(null=True)
    worldwide_id_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'm2epro_amazon_template_description'

class M2EproAmazonTemplateDescriptionDefinition(BaseModel):
    brand_custom_attribute = CharField(null=True)
    brand_custom_value = CharField(null=True)
    brand_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    bullet_points = TextField()
    bullet_points_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_date = DateTimeField(null=True)
    description_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    description_template = TextField()
    gallery_images_attribute = CharField()
    gallery_images_limit = IntegerField(constraints=[SQL("DEFAULT 1")])
    gallery_images_mode = IntegerField()
    image_main_attribute = CharField()
    image_main_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    image_variation_difference_attribute = CharField()
    image_variation_difference_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    item_dimensions_volume_height_custom_attribute = CharField(null=True)
    item_dimensions_volume_height_custom_value = CharField(null=True)
    item_dimensions_volume_length_custom_attribute = CharField(null=True)
    item_dimensions_volume_length_custom_value = CharField(null=True)
    item_dimensions_volume_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    item_dimensions_volume_unit_of_measure_custom_attribute = CharField(null=True)
    item_dimensions_volume_unit_of_measure_custom_value = CharField(null=True)
    item_dimensions_volume_unit_of_measure_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    item_dimensions_volume_width_custom_attribute = CharField(null=True)
    item_dimensions_volume_width_custom_value = CharField(null=True)
    item_dimensions_weight_custom_attribute = CharField(null=True)
    item_dimensions_weight_custom_value = DecimalField(null=True)
    item_dimensions_weight_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    item_dimensions_weight_unit_of_measure_custom_attribute = CharField(null=True)
    item_dimensions_weight_unit_of_measure_custom_value = CharField(null=True)
    item_dimensions_weight_unit_of_measure_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    item_package_quantity_custom_attribute = CharField(null=True)
    item_package_quantity_custom_value = CharField(null=True)
    item_package_quantity_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    manufacturer_custom_attribute = CharField(null=True)
    manufacturer_custom_value = CharField(null=True)
    manufacturer_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    manufacturer_part_number_custom_attribute = CharField()
    manufacturer_part_number_custom_value = CharField()
    manufacturer_part_number_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    number_of_items_custom_attribute = CharField(null=True)
    number_of_items_custom_value = CharField(null=True)
    number_of_items_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    package_dimensions_volume_height_custom_attribute = CharField(null=True)
    package_dimensions_volume_height_custom_value = CharField(null=True)
    package_dimensions_volume_length_custom_attribute = CharField(null=True)
    package_dimensions_volume_length_custom_value = CharField(null=True)
    package_dimensions_volume_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    package_dimensions_volume_unit_of_measure_custom_attribute = CharField(null=True)
    package_dimensions_volume_unit_of_measure_custom_value = CharField(null=True)
    package_dimensions_volume_unit_of_measure_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    package_dimensions_volume_width_custom_attribute = CharField(null=True)
    package_dimensions_volume_width_custom_value = CharField(null=True)
    package_weight_custom_attribute = CharField(null=True)
    package_weight_custom_value = DecimalField(null=True)
    package_weight_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    package_weight_unit_of_measure_custom_attribute = CharField(null=True)
    package_weight_unit_of_measure_custom_value = CharField(null=True)
    package_weight_unit_of_measure_mode = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    search_terms = TextField()
    search_terms_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipping_weight_custom_attribute = CharField(null=True)
    shipping_weight_custom_value = DecimalField(null=True)
    shipping_weight_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    shipping_weight_unit_of_measure_custom_attribute = CharField(null=True)
    shipping_weight_unit_of_measure_custom_value = CharField(null=True)
    shipping_weight_unit_of_measure_mode = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    target_audience = TextField()
    target_audience_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    template_description_id = AutoField()
    title_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    title_template = CharField()
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_amazon_template_description_definition'

class M2EproAmazonTemplateDescriptionSpecific(BaseModel):
    attributes = TextField(null=True)
    create_date = DateTimeField(null=True)
    custom_attribute = CharField(null=True)
    custom_value = CharField(null=True)
    is_required = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    mode = CharField()
    recommended_value = CharField(null=True)
    template_description_id = IntegerField(index=True)
    type = CharField(null=True)
    update_date = DateTimeField(null=True)
    xpath = CharField()

    class Meta:
        table_name = 'm2epro_amazon_template_description_specific'

class M2EproAmazonTemplateSellingFormat(BaseModel):
    map_price_custom_attribute = CharField()
    map_price_mode = IntegerField()
    price_coefficient = CharField()
    price_custom_attribute = CharField()
    price_mode = IntegerField()
    price_variation_mode = IntegerField(index=True)
    price_vat_percent = FloatField(constraints=[SQL("DEFAULT 0")])
    qty_custom_attribute = CharField()
    qty_custom_value = IntegerField()
    qty_max_posted_value = IntegerField(null=True)
    qty_min_posted_value = IntegerField(null=True)
    qty_mode = IntegerField()
    qty_modification_mode = IntegerField()
    qty_percentage = IntegerField(constraints=[SQL("DEFAULT 100")])
    sale_price_coefficient = CharField()
    sale_price_custom_attribute = CharField()
    sale_price_end_date_custom_attribute = CharField()
    sale_price_end_date_mode = IntegerField()
    sale_price_end_date_value = DateTimeField()
    sale_price_mode = IntegerField()
    sale_price_start_date_custom_attribute = CharField()
    sale_price_start_date_mode = IntegerField()
    sale_price_start_date_value = DateTimeField()
    template_selling_format_id = AutoField()

    class Meta:
        table_name = 'm2epro_amazon_template_selling_format'

class M2EproAmazonTemplateShippingOverride(BaseModel):
    create_date = DateTimeField(null=True)
    marketplace_id = IntegerField(index=True)
    title = CharField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_amazon_template_shipping_override'

class M2EproAmazonTemplateShippingOverrideService(BaseModel):
    cost_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    cost_value = CharField()
    location = CharField()
    option = CharField()
    service = CharField()
    template_shipping_override_id = IntegerField(index=True)
    type = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'm2epro_amazon_template_shipping_override_service'

class M2EproAmazonTemplateSynchronization(BaseModel):
    list_is_in_stock = IntegerField()
    list_mode = IntegerField()
    list_qty_calculated = IntegerField()
    list_qty_calculated_value = IntegerField()
    list_qty_calculated_value_max = IntegerField()
    list_qty_magento = IntegerField()
    list_qty_magento_value = IntegerField()
    list_qty_magento_value_max = IntegerField()
    list_status_enabled = IntegerField()
    relist_filter_user_lock = IntegerField()
    relist_is_in_stock = IntegerField()
    relist_mode = IntegerField()
    relist_qty_calculated = IntegerField()
    relist_qty_calculated_value = IntegerField()
    relist_qty_calculated_value_max = IntegerField()
    relist_qty_magento = IntegerField()
    relist_qty_magento_value = IntegerField()
    relist_qty_magento_value_max = IntegerField()
    relist_send_data = IntegerField()
    relist_status_enabled = IntegerField()
    revise_change_description_template = IntegerField()
    revise_change_shipping_override_template = IntegerField()
    revise_update_details = IntegerField()
    revise_update_images = IntegerField()
    revise_update_price = IntegerField()
    revise_update_price_max_allowed_deviation = IntegerField(null=True)
    revise_update_price_max_allowed_deviation_mode = IntegerField()
    revise_update_qty = IntegerField()
    revise_update_qty_max_applied_value = IntegerField(null=True)
    revise_update_qty_max_applied_value_mode = IntegerField()
    stop_out_off_stock = IntegerField()
    stop_qty_calculated = IntegerField()
    stop_qty_calculated_value = IntegerField()
    stop_qty_calculated_value_max = IntegerField()
    stop_qty_magento = IntegerField()
    stop_qty_magento_value = IntegerField()
    stop_qty_magento_value_max = IntegerField()
    stop_status_disabled = IntegerField()
    template_synchronization_id = AutoField()

    class Meta:
        table_name = 'm2epro_amazon_template_synchronization'

class M2EproBuyAccount(BaseModel):
    account_id = AutoField()
    ftp_inventory_access = IntegerField(constraints=[SQL("DEFAULT 0")])
    ftp_login = CharField()
    ftp_new_sku_access = IntegerField(constraints=[SQL("DEFAULT 0")])
    ftp_orders_access = IntegerField(constraints=[SQL("DEFAULT 0")])
    info = TextField(null=True)
    magento_orders_settings = TextField()
    orders_last_synchronization = DateTimeField(null=True)
    other_listings_mapping_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    other_listings_mapping_settings = CharField(null=True)
    other_listings_move_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    other_listings_move_settings = CharField(null=True)
    other_listings_synchronization = IntegerField(constraints=[SQL("DEFAULT 1")])
    related_store_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    seller_id = CharField(null=True)
    server_hash = CharField()
    web_login = CharField()

    class Meta:
        table_name = 'm2epro_buy_account'

class M2EproBuyDictionaryCategory(BaseModel):
    attributes = TextField(null=True)
    category_id = IntegerField(index=True)
    is_leaf = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    native_id = CharField(index=True, null=True)
    node_id = IntegerField(index=True)
    parent_category_id = IntegerField(index=True, null=True)
    path = CharField(index=True, null=True)
    title = CharField(index=True)

    class Meta:
        table_name = 'm2epro_buy_dictionary_category'

class M2EproBuyItem(BaseModel):
    account_id = IntegerField(index=True)
    create_date = DateTimeField(null=True)
    marketplace_id = IntegerField(index=True)
    product_id = IntegerField(index=True)
    sku = CharField(index=True)
    store_id = IntegerField(index=True)
    update_date = DateTimeField(null=True)
    variation_product_options = TextField(null=True)

    class Meta:
        table_name = 'm2epro_buy_item'

class M2EproBuyListing(BaseModel):
    condition_custom_attribute = CharField()
    condition_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    condition_note_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    condition_note_value = TextField()
    condition_value = CharField()
    general_id_custom_attribute = CharField()
    general_id_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    generate_sku_mode = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    listing_id = AutoField()
    search_by_magento_title_mode = IntegerField(constraints=[SQL("DEFAULT 1")])
    shipping_expedited_custom_attribute = CharField()
    shipping_expedited_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipping_expedited_value = DecimalField()
    shipping_one_day_custom_attribute = CharField()
    shipping_one_day_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipping_one_day_value = DecimalField()
    shipping_standard_custom_attribute = CharField()
    shipping_standard_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipping_standard_value = DecimalField()
    shipping_two_day_custom_attribute = CharField()
    shipping_two_day_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipping_two_day_value = DecimalField()
    sku_custom_attribute = CharField()
    sku_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    sku_modification_custom_value = CharField()
    sku_modification_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    template_selling_format_id = IntegerField(index=True)
    template_synchronization_id = IntegerField(index=True)

    class Meta:
        table_name = 'm2epro_buy_listing'

class M2EproBuyListingAutoCategoryGroup(BaseModel):
    listing_auto_category_group_id = AutoField()

    class Meta:
        table_name = 'm2epro_buy_listing_auto_category_group'

class M2EproBuyListingOther(BaseModel):
    condition = IntegerField(index=True)
    condition_note = CharField()
    general_id = IntegerField(index=True)
    listing_other_id = AutoField()
    online_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")], index=True)
    online_qty = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    shipping_expedited_mode = IntegerField(index=True)
    shipping_expedited_rate = DecimalField(index=True)
    shipping_standard_rate = DecimalField(index=True)
    sku = CharField(index=True)
    title = CharField(index=True, null=True)

    class Meta:
        table_name = 'm2epro_buy_listing_other'

class M2EproBuyListingProduct(BaseModel):
    condition = IntegerField(index=True, null=True)
    condition_note = CharField(null=True)
    general_id = IntegerField(index=True, null=True)
    general_id_search_info = TextField(null=True)
    is_variation_product = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_variation_product_matched = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    listing_product_id = AutoField()
    online_price = DecimalField(index=True, null=True)
    online_qty = IntegerField(index=True, null=True)
    search_settings_data = TextField(null=True)
    search_settings_status = IntegerField(index=True, null=True)
    shipping_expedited_mode = IntegerField(index=True, null=True)
    shipping_expedited_rate = DecimalField(index=True, null=True)
    shipping_standard_rate = DecimalField(index=True, null=True)
    sku = CharField(index=True, null=True)
    template_new_product_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'm2epro_buy_listing_product'

class M2EproBuyListingProductVariation(BaseModel):
    listing_product_variation_id = AutoField()

    class Meta:
        table_name = 'm2epro_buy_listing_product_variation'

class M2EproBuyListingProductVariationOption(BaseModel):
    listing_product_variation_option_id = AutoField()

    class Meta:
        table_name = 'm2epro_buy_listing_product_variation_option'

class M2EproBuyMarketplace(BaseModel):
    marketplace_id = AutoField()

    class Meta:
        table_name = 'm2epro_buy_marketplace'

class M2EproBuyOrder(BaseModel):
    billing_address = TextField()
    buy_order_id = IntegerField(index=True)
    buyer_email = CharField(index=True, null=True)
    buyer_name = CharField(index=True)
    currency = CharField()
    order_id = AutoField()
    paid_amount = DecimalField(index=True)
    purchase_create_date = DateTimeField(null=True)
    seller_id = IntegerField()
    shipping_address = TextField()
    shipping_method = CharField(null=True)
    shipping_price = DecimalField()

    class Meta:
        table_name = 'm2epro_buy_order'

class M2EproBuyOrderItem(BaseModel):
    buy_order_item_id = IntegerField(index=True)
    commission = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    currency = CharField()
    general_id = IntegerField(index=True)
    order_item_id = AutoField()
    per_item_fee = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    product_owed = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    qty_cancelled = IntegerField(constraints=[SQL("DEFAULT 0")])
    qty_shipped = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipping_fee = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    shipping_owed = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    sku = CharField(index=True, null=True)
    tax_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    title = CharField(index=True, null=True)

    class Meta:
        table_name = 'm2epro_buy_order_item'

class M2EproBuyTemplateNewProduct(BaseModel):
    category_id = IntegerField()
    category_path = CharField()
    create_date = DateTimeField(null=True)
    node_title = CharField()
    title = CharField(constraints=[SQL("DEFAULT 'Default'")])
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_buy_template_new_product'

class M2EproBuyTemplateNewProductAttribute(BaseModel):
    attribute_name = CharField()
    create_date = DateTimeField(null=True)
    custom_attribute = CharField(null=True)
    custom_value = TextField(null=True)
    mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    recommended_value = TextField(null=True)
    template_new_product_id = IntegerField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_buy_template_new_product_attribute'

class M2EproBuyTemplateNewProductCore(BaseModel):
    additional_images_attribute = CharField(null=True)
    additional_images_limit = IntegerField(null=True)
    additional_images_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_date = DateTimeField(null=True)
    description_mode = IntegerField()
    description_template = TextField()
    features_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    features_template = TextField(null=True)
    gtin_custom_attribute = CharField(null=True)
    gtin_mode = IntegerField(constraints=[SQL("DEFAULT 2")])
    isbn_custom_attribute = CharField(null=True)
    isbn_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    keywords_custom_attribute = CharField(null=True)
    keywords_custom_value = CharField(null=True)
    keywords_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    main_image_attribute = CharField()
    main_image_mode = IntegerField()
    mfg_name_template = CharField()
    mfg_part_number_custom_attribute = CharField(null=True)
    mfg_part_number_custom_value = CharField(null=True)
    mfg_part_number_mode = IntegerField()
    product_set_id_custom_attribute = CharField(null=True)
    product_set_id_custom_value = CharField(null=True)
    product_set_id_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    seller_sku_custom_attribute = CharField(null=True)
    template_new_product_id = AutoField()
    title_mode = IntegerField()
    title_template = CharField()
    update_date = DateTimeField(null=True)
    weight_custom_attribute = CharField(null=True)
    weight_custom_value = DecimalField(null=True)
    weight_mode = IntegerField(null=True)

    class Meta:
        table_name = 'm2epro_buy_template_new_product_core'

class M2EproBuyTemplateSellingFormat(BaseModel):
    price_coefficient = CharField()
    price_custom_attribute = CharField()
    price_mode = IntegerField()
    price_variation_mode = IntegerField(index=True)
    price_vat_percent = FloatField(constraints=[SQL("DEFAULT 0")])
    qty_custom_attribute = CharField()
    qty_custom_value = IntegerField()
    qty_max_posted_value = IntegerField(null=True)
    qty_min_posted_value = IntegerField(null=True)
    qty_mode = IntegerField()
    qty_modification_mode = IntegerField()
    qty_percentage = IntegerField(constraints=[SQL("DEFAULT 100")])
    template_selling_format_id = AutoField()

    class Meta:
        table_name = 'm2epro_buy_template_selling_format'

class M2EproBuyTemplateSynchronization(BaseModel):
    list_is_in_stock = IntegerField()
    list_mode = IntegerField()
    list_qty_calculated = IntegerField()
    list_qty_calculated_value = IntegerField()
    list_qty_calculated_value_max = IntegerField()
    list_qty_magento = IntegerField()
    list_qty_magento_value = IntegerField()
    list_qty_magento_value_max = IntegerField()
    list_status_enabled = IntegerField()
    relist_filter_user_lock = IntegerField()
    relist_is_in_stock = IntegerField()
    relist_mode = IntegerField()
    relist_qty_calculated = IntegerField()
    relist_qty_calculated_value = IntegerField()
    relist_qty_calculated_value_max = IntegerField()
    relist_qty_magento = IntegerField()
    relist_qty_magento_value = IntegerField()
    relist_qty_magento_value_max = IntegerField()
    relist_status_enabled = IntegerField()
    revise_update_price = IntegerField()
    revise_update_price_max_allowed_deviation = IntegerField(null=True)
    revise_update_price_max_allowed_deviation_mode = IntegerField()
    revise_update_qty = IntegerField()
    revise_update_qty_max_applied_value = IntegerField(null=True)
    revise_update_qty_max_applied_value_mode = IntegerField()
    stop_out_off_stock = IntegerField()
    stop_qty_calculated = IntegerField()
    stop_qty_calculated_value = IntegerField()
    stop_qty_calculated_value_max = IntegerField()
    stop_qty_magento = IntegerField()
    stop_qty_magento_value = IntegerField()
    stop_qty_magento_value_max = IntegerField()
    stop_status_disabled = IntegerField()
    template_synchronization_id = AutoField()

    class Meta:
        table_name = 'm2epro_buy_template_synchronization'

class M2EproBv630AmazonTemplateNewProduct(BaseModel):
    category_path = CharField()
    create_date = DateTimeField(null=True)
    identifiers = CharField()
    item_package_quantity_custom_attribute = CharField(null=True)
    item_package_quantity_custom_value = CharField(null=True)
    item_package_quantity_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    marketplace_id = IntegerField(index=True)
    node_title = CharField()
    number_of_items_custom_attribute = CharField(null=True)
    number_of_items_custom_value = CharField(null=True)
    number_of_items_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    registered_parameter = CharField(null=True)
    title = CharField(constraints=[SQL("DEFAULT 'Default'")])
    update_date = DateTimeField(null=True)
    worldwide_id_custom_attribute = CharField(null=True)
    worldwide_id_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    xsd_hash = CharField()

    class Meta:
        table_name = 'm2epro_bv630_amazon_template_new_product'

class M2EproBv630AmazonTemplateNewProductDescription(BaseModel):
    brand_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    brand_template = CharField()
    bullet_points = TextField()
    bullet_points_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_date = DateTimeField(null=True)
    description_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    description_template = TextField()
    gallery_images_attribute = CharField()
    gallery_images_limit = IntegerField(constraints=[SQL("DEFAULT 1")])
    gallery_images_mode = IntegerField()
    image_main_attribute = CharField()
    image_main_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    manufacturer_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    manufacturer_part_number_custom_attribute = CharField()
    manufacturer_part_number_custom_value = CharField()
    manufacturer_part_number_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    manufacturer_template = CharField()
    package_weight_custom_attribute = CharField(null=True)
    package_weight_custom_value = DecimalField(null=True)
    package_weight_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    package_weight_unit_of_measure_custom_attribute = CharField(null=True)
    package_weight_unit_of_measure_custom_value = CharField(null=True)
    package_weight_unit_of_measure_mode = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    search_terms = TextField()
    search_terms_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipping_weight_custom_attribute = CharField(null=True)
    shipping_weight_custom_value = DecimalField(null=True)
    shipping_weight_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    shipping_weight_unit_of_measure_custom_attribute = CharField(null=True)
    shipping_weight_unit_of_measure_custom_value = CharField(null=True)
    shipping_weight_unit_of_measure_mode = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    target_audience_custom_attribute = CharField()
    target_audience_custom_value = CharField()
    target_audience_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    template_new_product_id = AutoField()
    title_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    title_template = CharField()
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_bv630_amazon_template_new_product_description'

class M2EproBv630AmazonTemplateNewProductSpecific(BaseModel):
    attributes = TextField(null=True)
    create_date = DateTimeField(null=True)
    custom_attribute = CharField(null=True)
    custom_value = CharField(null=True)
    mode = CharField()
    recommended_value = CharField(null=True)
    template_new_product_id = IntegerField(index=True)
    type = CharField(null=True)
    update_date = DateTimeField(null=True)
    xpath = CharField()

    class Meta:
        table_name = 'm2epro_bv630_amazon_template_new_product_specific'

class M2EproBv630EbayTemplateDescription(BaseModel):
    condition_attribute = CharField()
    condition_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    condition_note_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    condition_note_template = TextField()
    condition_value = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_date = DateTimeField(null=True)
    cut_long_titles = IntegerField(constraints=[SQL("DEFAULT 0")])
    default_image_url = CharField(null=True)
    description_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    description_template = TextField()
    editor_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    enhancement = CharField()
    gallery_images_attribute = CharField()
    gallery_images_limit = IntegerField(constraints=[SQL("DEFAULT 1")])
    gallery_images_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    gallery_type = IntegerField(constraints=[SQL("DEFAULT 4")])
    hit_counter = CharField()
    image_main_attribute = CharField()
    image_main_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_custom_template = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    product_details = TextField(null=True)
    subtitle_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    subtitle_template = CharField()
    title = CharField(index=True)
    title_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    title_template = CharField()
    update_date = DateTimeField(null=True)
    use_supersize_images = IntegerField(constraints=[SQL("DEFAULT 0")])
    variation_configurable_images = CharField()
    watermark_image = TextField(null=True)
    watermark_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    watermark_settings = TextField(null=True)

    class Meta:
        table_name = 'm2epro_bv630_ebay_template_description'

class M2EproCacheConfig(BaseModel):
    create_date = DateTimeField(null=True)
    group = CharField(index=True, null=True)
    key = CharField(index=True)
    notice = TextField(null=True)
    update_date = DateTimeField(null=True)
    value = CharField(index=True, null=True)

    class Meta:
        table_name = 'm2epro_cache_config'

class M2EproConfig(BaseModel):
    create_date = DateTimeField(null=True)
    group = CharField(index=True, null=True)
    key = CharField(index=True)
    notice = TextField(null=True)
    update_date = DateTimeField(null=True)
    value = CharField(index=True, null=True)

    class Meta:
        table_name = 'm2epro_config'

class M2EproEbayAccount(BaseModel):
    account_id = AutoField()
    defaults_last_synchronization = DateTimeField(null=True)
    ebay_shipping_discount_profiles = TextField(null=True)
    ebay_store_description = TextField()
    ebay_store_subscription_level = CharField()
    ebay_store_title = CharField()
    ebay_store_url = TextField()
    feedbacks_auto_response = IntegerField(constraints=[SQL("DEFAULT 0")])
    feedbacks_auto_response_only_positive = IntegerField(constraints=[SQL("DEFAULT 0")])
    feedbacks_last_used_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    feedbacks_receive = IntegerField(constraints=[SQL("DEFAULT 0")])
    info = TextField(null=True)
    magento_orders_settings = TextField()
    marketplaces_data = TextField(null=True)
    messages_receive = IntegerField(constraints=[SQL("DEFAULT 0")])
    mode = IntegerField()
    orders_last_synchronization = DateTimeField(null=True)
    other_listings_last_synchronization = DateTimeField(null=True)
    other_listings_mapping_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    other_listings_mapping_settings = CharField(null=True)
    other_listings_synchronization = IntegerField(constraints=[SQL("DEFAULT 1")])
    server_hash = CharField()
    token_expired_date = DateTimeField()
    token_session = CharField()
    translation_hash = CharField(null=True)
    translation_info = TextField(null=True)
    user_id = CharField()

    class Meta:
        table_name = 'm2epro_ebay_account'

class M2EproEbayAccountStoreCategory(BaseModel):
    account_id = IntegerField()
    category_id = DecimalField()
    is_leaf = IntegerField(constraints=[SQL("DEFAULT 0")])
    parent_id = DecimalField(index=True)
    sorder = IntegerField(index=True)
    title = CharField(index=True)

    class Meta:
        table_name = 'm2epro_ebay_account_store_category'
        indexes = (
            (('account_id', 'category_id'), True),
        )
        primary_key = CompositeKey('account_id', 'category_id')

class M2EproEbayDictionaryCategory(BaseModel):
    category_id = IntegerField(index=True)
    features = TextField(null=True)
    is_leaf = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    item_specifics = TextField(null=True)
    marketplace_id = IntegerField(index=True)
    parent_category_id = IntegerField(index=True, null=True)
    path = CharField(index=True, null=True)
    title = CharField(index=True)

    class Meta:
        table_name = 'm2epro_ebay_dictionary_category'

class M2EproEbayDictionaryMarketplace(BaseModel):
    additional_data = TextField(null=True)
    charities = TextField()
    client_details_last_update_date = DateTimeField(null=True)
    dispatch = TextField()
    listing_features = TextField()
    marketplace_id = IntegerField(index=True)
    packages = TextField()
    payments = TextField()
    return_policy = TextField()
    server_details_last_update_date = DateTimeField(null=True)
    shipping_locations = TextField()
    shipping_locations_exclude = TextField()
    tax_categories = TextField()

    class Meta:
        table_name = 'm2epro_ebay_dictionary_marketplace'

class M2EproEbayDictionaryMotorEpid(BaseModel):
    engine = CharField(index=True, null=True)
    epid = CharField(index=True)
    is_custom = IntegerField(index=True)
    make = CharField(index=True)
    model = CharField(index=True)
    product_type = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    submodel = CharField(index=True, null=True)
    trim = CharField(index=True, null=True)
    year = IntegerField(index=True)

    class Meta:
        table_name = 'm2epro_ebay_dictionary_motor_epid'

class M2EproEbayDictionaryMotorKtype(BaseModel):
    body_style = CharField(index=True, null=True)
    engine = CharField(index=True, null=True)
    from_year = IntegerField(index=True, null=True)
    is_custom = IntegerField(index=True)
    ktype = IntegerField(index=True)
    make = CharField(index=True, null=True)
    model = CharField(index=True, null=True)
    to_year = IntegerField(index=True, null=True)
    type = CharField(index=True, null=True)
    variant = CharField(index=True, null=True)

    class Meta:
        table_name = 'm2epro_ebay_dictionary_motor_ktype'

class M2EproEbayDictionaryShipping(BaseModel):
    category = CharField(index=True)
    data = TextField()
    ebay_id = CharField(index=True)
    is_calculated = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_flat = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_international = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    marketplace_id = IntegerField(index=True)
    title = CharField(index=True)

    class Meta:
        table_name = 'm2epro_ebay_dictionary_shipping'

class M2EproEbayFeedback(BaseModel):
    account_id = IntegerField(index=True)
    buyer_feedback_date = DateTimeField()
    buyer_feedback_id = DecimalField(index=True)
    buyer_feedback_text = CharField()
    buyer_feedback_type = CharField()
    buyer_name = CharField()
    create_date = DateTimeField(null=True)
    ebay_item_id = DecimalField(index=True)
    ebay_item_title = CharField()
    ebay_transaction_id = CharField(index=True)
    last_response_attempt_date = DateTimeField(null=True)
    seller_feedback_date = DateTimeField()
    seller_feedback_id = DecimalField(index=True)
    seller_feedback_text = CharField()
    seller_feedback_type = CharField()
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_feedback'

class M2EproEbayFeedbackTemplate(BaseModel):
    account_id = IntegerField(index=True)
    body = TextField()
    create_date = DateTimeField(null=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_feedback_template'

class M2EproEbayItem(BaseModel):
    account_id = IntegerField(index=True)
    create_date = DateTimeField(null=True)
    item_id = DecimalField(index=True)
    marketplace_id = IntegerField(index=True)
    product_id = IntegerField(index=True)
    store_id = IntegerField(index=True)
    update_date = DateTimeField(null=True)
    variations = TextField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_item'

class M2EproEbayListing(BaseModel):
    auto_global_adding_template_category_id = IntegerField(index=True, null=True)
    auto_global_adding_template_other_category_id = IntegerField(index=True, null=True)
    auto_website_adding_template_category_id = IntegerField(index=True, null=True)
    auto_website_adding_template_other_category_id = IntegerField(index=True, null=True)
    items_sold_count = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    listing_id = AutoField()
    product_add_ids = TextField(null=True)
    products_sold_count = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    template_description_custom_id = IntegerField(index=True, null=True)
    template_description_id = IntegerField(index=True, null=True)
    template_description_mode = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    template_payment_custom_id = IntegerField(index=True, null=True)
    template_payment_id = IntegerField(index=True, null=True)
    template_payment_mode = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    template_return_custom_id = IntegerField(index=True, null=True)
    template_return_id = IntegerField(index=True, null=True)
    template_return_mode = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    template_selling_format_custom_id = IntegerField(index=True, null=True)
    template_selling_format_id = IntegerField(index=True, null=True)
    template_selling_format_mode = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    template_shipping_custom_id = IntegerField(index=True, null=True)
    template_shipping_id = IntegerField(index=True, null=True)
    template_shipping_mode = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    template_synchronization_custom_id = IntegerField(index=True, null=True)
    template_synchronization_id = IntegerField(index=True, null=True)
    template_synchronization_mode = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)

    class Meta:
        table_name = 'm2epro_ebay_listing'

class M2EproEbayListingAutoCategoryGroup(BaseModel):
    adding_template_category_id = IntegerField(index=True, null=True)
    adding_template_other_category_id = IntegerField(index=True, null=True)
    listing_auto_category_group_id = AutoField()

    class Meta:
        table_name = 'm2epro_ebay_listing_auto_category_group'

class M2EproEbayListingOther(BaseModel):
    currency = CharField(index=True, null=True)
    end_date = DateTimeField(index=True, null=True)
    item_id = DecimalField(index=True)
    listing_other_id = AutoField()
    old_items = TextField(null=True)
    online_bids = IntegerField(index=True, null=True)
    online_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")], index=True)
    online_qty = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    online_qty_sold = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    sku = CharField(index=True, null=True)
    start_date = DateTimeField(index=True)
    title = CharField(index=True)

    class Meta:
        table_name = 'm2epro_ebay_listing_other'

class M2EproEbayListingProduct(BaseModel):
    ebay_item_id = IntegerField(index=True, null=True)
    end_date = DateTimeField(index=True, null=True)
    listing_product_id = AutoField()
    online_bids = IntegerField(index=True, null=True)
    online_buyitnow_price = DecimalField(index=True, null=True)
    online_category = CharField(index=True, null=True)
    online_current_price = DecimalField(index=True, null=True)
    online_qty = IntegerField(index=True, null=True)
    online_qty_sold = IntegerField(index=True, null=True)
    online_reserve_price = DecimalField(index=True, null=True)
    online_sku = CharField(index=True, null=True)
    online_start_price = DecimalField(index=True, null=True)
    online_title = CharField(index=True, null=True)
    start_date = DateTimeField(index=True, null=True)
    template_category_id = IntegerField(index=True, null=True)
    template_description_custom_id = IntegerField(index=True, null=True)
    template_description_id = IntegerField(index=True, null=True)
    template_description_mode = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    template_other_category_id = IntegerField(index=True, null=True)
    template_payment_custom_id = IntegerField(index=True, null=True)
    template_payment_id = IntegerField(index=True, null=True)
    template_payment_mode = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    template_return_custom_id = IntegerField(index=True, null=True)
    template_return_id = IntegerField(index=True, null=True)
    template_return_mode = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    template_selling_format_custom_id = IntegerField(index=True, null=True)
    template_selling_format_id = IntegerField(index=True, null=True)
    template_selling_format_mode = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    template_shipping_custom_id = IntegerField(index=True, null=True)
    template_shipping_id = IntegerField(index=True, null=True)
    template_shipping_mode = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    template_synchronization_custom_id = IntegerField(index=True, null=True)
    template_synchronization_id = IntegerField(index=True, null=True)
    template_synchronization_mode = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    translated_date = DateTimeField(index=True, null=True)
    translation_service = CharField(index=True, null=True)
    translation_status = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'm2epro_ebay_listing_product'

class M2EproEbayListingProductVariation(BaseModel):
    add = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delete = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    listing_product_variation_id = AutoField()
    online_price = DecimalField(index=True, null=True)
    online_qty = IntegerField(index=True, null=True)
    online_qty_sold = IntegerField(index=True, null=True)
    online_sku = CharField(index=True, null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'm2epro_ebay_listing_product_variation'

class M2EproEbayListingProductVariationOption(BaseModel):
    listing_product_variation_option_id = AutoField()

    class Meta:
        table_name = 'm2epro_ebay_listing_product_variation_option'

class M2EproEbayMarketplace(BaseModel):
    currency = CharField(constraints=[SQL("DEFAULT 'USD'")])
    is_calculated_shipping = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_cash_on_delivery = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_charity = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_click_and_collect = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_english_measurement_system = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_freight_shipping = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_global_shipping_program = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_holiday_return = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_international_shipping_rate_table = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_local_shipping_rate_table = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_map = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_metric_measurement_system = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_multi_currency = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_multivariation = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_stp = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_stp_advanced = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_tax_table = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    is_vat = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    language_code = CharField(null=True)
    marketplace_id = AutoField()
    origin_country = CharField(null=True)
    translation_service_mode = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'm2epro_ebay_marketplace'

class M2EproEbayMotorFilter(BaseModel):
    conditions = TextField()
    create_date = DateTimeField(null=True)
    note = TextField(null=True)
    title = CharField()
    type = IntegerField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_motor_filter'

class M2EproEbayMotorFilterToGroup(BaseModel):
    filter_id = IntegerField(index=True)
    group_id = IntegerField(index=True)

    class Meta:
        table_name = 'm2epro_ebay_motor_filter_to_group'

class M2EproEbayMotorGroup(BaseModel):
    create_date = DateTimeField(null=True)
    items_data = TextField(null=True)
    mode = IntegerField(index=True)
    title = CharField()
    type = IntegerField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_motor_group'

class M2EproEbayOrder(BaseModel):
    buyer_email = CharField(index=True)
    buyer_message = CharField(null=True)
    buyer_name = CharField(index=True)
    buyer_tax_id = CharField(null=True)
    buyer_user_id = CharField(index=True)
    checkout_status = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    currency = CharField()
    ebay_order_id = CharField(index=True)
    order_id = AutoField()
    paid_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], index=True)
    payment_details = TextField(null=True)
    payment_status = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    purchase_create_date = DateTimeField(null=True)
    purchase_update_date = DateTimeField(null=True)
    saved_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    selling_manager_id = IntegerField(index=True, null=True)
    shipping_details = TextField(null=True)
    shipping_status = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    tax_details = TextField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_order'

class M2EproEbayOrderExternalTransaction(BaseModel):
    create_date = DateTimeField(null=True)
    fee = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    is_refund = IntegerField(constraints=[SQL("DEFAULT 0")])
    order_id = IntegerField(index=True)
    sum = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    transaction_date = DateTimeField()
    transaction_id = CharField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_order_external_transaction'

class M2EproEbayOrderItem(BaseModel):
    final_fee = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    item_id = DecimalField(index=True)
    order_item_id = AutoField()
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    qty_purchased = IntegerField()
    selling_manager_id = IntegerField(index=True, null=True)
    sku = CharField(index=True, null=True)
    tax_details = TextField(null=True)
    title = CharField(index=True)
    tracking_details = TextField(null=True)
    transaction_id = CharField(index=True)
    unpaid_item_process_state = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    variation_details = TextField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_order_item'

class M2EproEbayTemplateCategory(BaseModel):
    category_main_attribute = CharField()
    category_main_id = IntegerField()
    category_main_mode = IntegerField(constraints=[SQL("DEFAULT 2")])
    category_main_path = CharField(null=True)
    create_date = DateTimeField(null=True)
    marketplace_id = IntegerField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_template_category'

class M2EproEbayTemplateCategorySpecific(BaseModel):
    attribute_title = CharField()
    mode = IntegerField(constraints=[SQL("DEFAULT 1")])
    template_category_id = IntegerField(index=True)
    value_custom_attribute = CharField(null=True)
    value_custom_value = CharField(null=True)
    value_ebay_recommended = TextField(null=True)
    value_mode = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'm2epro_ebay_template_category_specific'

class M2EproEbayTemplateDescription(BaseModel):
    condition_attribute = CharField()
    condition_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    condition_note_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    condition_note_template = TextField()
    condition_value = IntegerField(constraints=[SQL("DEFAULT 0")])
    cut_long_titles = IntegerField(constraints=[SQL("DEFAULT 0")])
    default_image_url = CharField(null=True)
    description_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    description_template = TextField()
    editor_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    enhancement = CharField()
    gallery_images_attribute = CharField()
    gallery_images_limit = IntegerField(constraints=[SQL("DEFAULT 1")])
    gallery_images_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    gallery_type = IntegerField(constraints=[SQL("DEFAULT 4")])
    hit_counter = CharField()
    image_main_attribute = CharField()
    image_main_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_custom_template = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    product_details = TextField(null=True)
    subtitle_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    subtitle_template = CharField()
    template_description_id = AutoField()
    title_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    title_template = CharField()
    use_supersize_images = IntegerField(constraints=[SQL("DEFAULT 0")])
    variation_configurable_images = TextField(null=True)
    variation_images_attribute = CharField()
    variation_images_limit = IntegerField(constraints=[SQL("DEFAULT 1")])
    variation_images_mode = IntegerField(constraints=[SQL("DEFAULT 1")])
    watermark_image = TextField(null=True)
    watermark_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    watermark_settings = TextField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_template_description'

class M2EproEbayTemplateOtherCategory(BaseModel):
    account_id = IntegerField(index=True)
    category_secondary_attribute = CharField()
    category_secondary_id = IntegerField()
    category_secondary_mode = IntegerField(constraints=[SQL("DEFAULT 2")])
    category_secondary_path = CharField(null=True)
    create_date = DateTimeField(null=True)
    marketplace_id = IntegerField(index=True)
    store_category_main_attribute = CharField()
    store_category_main_id = DecimalField()
    store_category_main_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    store_category_main_path = CharField(null=True)
    store_category_secondary_attribute = CharField()
    store_category_secondary_id = DecimalField()
    store_category_secondary_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    store_category_secondary_path = CharField(null=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_template_other_category'

class M2EproEbayTemplatePayment(BaseModel):
    create_date = DateTimeField(null=True)
    is_custom_template = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    marketplace_id = IntegerField(index=True)
    pay_pal_email_address = CharField()
    pay_pal_immediate_payment = IntegerField(constraints=[SQL("DEFAULT 0")])
    pay_pal_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    title = CharField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_template_payment'

class M2EproEbayTemplatePaymentService(BaseModel):
    code_name = CharField()
    template_payment_id = IntegerField(index=True)

    class Meta:
        table_name = 'm2epro_ebay_template_payment_service'

class M2EproEbayTemplateReturn(BaseModel):
    accepted = CharField()
    create_date = DateTimeField(null=True)
    description = TextField()
    holiday_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_custom_template = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    marketplace_id = IntegerField(index=True)
    option = CharField()
    restocking_fee = CharField()
    shipping_cost = CharField()
    title = CharField(index=True)
    update_date = DateTimeField(null=True)
    within = CharField()

    class Meta:
        table_name = 'm2epro_ebay_template_return'

class M2EproEbayTemplateSellingFormat(BaseModel):
    best_offer_accept_attribute = CharField()
    best_offer_accept_mode = IntegerField()
    best_offer_accept_value = CharField()
    best_offer_mode = IntegerField()
    best_offer_reject_attribute = CharField()
    best_offer_reject_mode = IntegerField()
    best_offer_reject_value = CharField()
    buyitnow_price_coefficient = CharField()
    buyitnow_price_custom_attribute = CharField()
    buyitnow_price_mode = IntegerField()
    charity = CharField(null=True)
    duration_attribute = CharField()
    duration_mode = IntegerField()
    fixed_price_coefficient = CharField()
    fixed_price_custom_attribute = CharField()
    fixed_price_mode = IntegerField()
    ignore_variations = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_custom_template = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    listing_is_private = IntegerField()
    listing_type = IntegerField()
    listing_type_attribute = CharField()
    out_of_stock_control = IntegerField(constraints=[SQL("DEFAULT 0")])
    price_discount_map_attribute = CharField()
    price_discount_map_exposure_type = IntegerField()
    price_discount_map_mode = IntegerField()
    price_discount_stp_attribute = CharField()
    price_discount_stp_mode = IntegerField()
    price_discount_stp_type = IntegerField()
    price_increase_vat_percent = IntegerField(constraints=[SQL("DEFAULT 0")])
    price_variation_mode = IntegerField()
    qty_custom_attribute = CharField()
    qty_custom_value = IntegerField()
    qty_max_posted_value = IntegerField(null=True)
    qty_min_posted_value = IntegerField(null=True)
    qty_mode = IntegerField()
    qty_modification_mode = IntegerField()
    qty_percentage = IntegerField(constraints=[SQL("DEFAULT 100")])
    reserve_price_coefficient = CharField()
    reserve_price_custom_attribute = CharField()
    reserve_price_mode = IntegerField()
    restricted_to_business = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    start_price_coefficient = CharField()
    start_price_custom_attribute = CharField()
    start_price_mode = IntegerField()
    tax_category_attribute = CharField()
    tax_category_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    tax_category_value = CharField()
    tax_table_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    template_selling_format_id = AutoField()
    vat_percent = FloatField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'm2epro_ebay_template_selling_format'

class M2EproEbayTemplateShipping(BaseModel):
    address_custom_attribute = CharField()
    address_custom_value = CharField()
    address_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    cash_on_delivery_cost = CharField(null=True)
    click_and_collect_mode = IntegerField(constraints=[SQL("DEFAULT 1")])
    country_custom_attribute = CharField()
    country_custom_value = CharField()
    country_mode = IntegerField(constraints=[SQL("DEFAULT 1")])
    create_date = DateTimeField(null=True)
    cross_border_trade = IntegerField(constraints=[SQL("DEFAULT 0")])
    dispatch_time = IntegerField(constraints=[SQL("DEFAULT 1")])
    excluded_locations = TextField(null=True)
    global_shipping_program = IntegerField(constraints=[SQL("DEFAULT 0")])
    international_shipping_discount_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    international_shipping_discount_profile_id = TextField(null=True)
    international_shipping_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    international_shipping_rate_table_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_custom_template = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    local_shipping_discount_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    local_shipping_discount_profile_id = TextField(null=True)
    local_shipping_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    local_shipping_rate_table_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    marketplace_id = IntegerField(index=True)
    postal_code_custom_attribute = CharField()
    postal_code_custom_value = CharField()
    postal_code_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    title = CharField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_ebay_template_shipping'

class M2EproEbayTemplateShippingCalculated(BaseModel):
    dimension_depth_attribute = CharField()
    dimension_depth_value = CharField()
    dimension_length_attribute = CharField()
    dimension_length_value = CharField()
    dimension_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    dimension_width_attribute = CharField()
    dimension_width_value = CharField()
    international_handling_cost = CharField(null=True)
    local_handling_cost = CharField(null=True)
    measurement_system = IntegerField(constraints=[SQL("DEFAULT 1")])
    package_size_attribute = CharField()
    package_size_mode = IntegerField(constraints=[SQL("DEFAULT 1")])
    package_size_value = CharField()
    template_shipping_id = AutoField()
    weight_attribute = CharField()
    weight_major = CharField()
    weight_minor = CharField()
    weight_mode = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'm2epro_ebay_template_shipping_calculated'

class M2EproEbayTemplateShippingService(BaseModel):
    cost_additional_value = CharField()
    cost_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    cost_surcharge_value = CharField()
    cost_value = CharField()
    locations = TextField()
    priority = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    shipping_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipping_value = CharField()
    template_shipping_id = IntegerField(index=True)

    class Meta:
        table_name = 'm2epro_ebay_template_shipping_service'

class M2EproEbayTemplateSynchronization(BaseModel):
    is_custom_template = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    list_is_in_stock = IntegerField()
    list_mode = IntegerField()
    list_qty_calculated = IntegerField()
    list_qty_calculated_value = IntegerField()
    list_qty_calculated_value_max = IntegerField()
    list_qty_magento = IntegerField()
    list_qty_magento_value = IntegerField()
    list_qty_magento_value_max = IntegerField()
    list_status_enabled = IntegerField()
    relist_filter_user_lock = IntegerField()
    relist_is_in_stock = IntegerField()
    relist_mode = IntegerField()
    relist_qty_calculated = IntegerField()
    relist_qty_calculated_value = IntegerField()
    relist_qty_calculated_value_max = IntegerField()
    relist_qty_magento = IntegerField()
    relist_qty_magento_value = IntegerField()
    relist_qty_magento_value_max = IntegerField()
    relist_send_data = IntegerField()
    relist_status_enabled = IntegerField()
    revise_change_category_template = IntegerField()
    revise_change_description_template = IntegerField()
    revise_change_payment_template = IntegerField()
    revise_change_return_template = IntegerField()
    revise_change_shipping_template = IntegerField()
    revise_update_description = IntegerField()
    revise_update_images = IntegerField()
    revise_update_price = IntegerField()
    revise_update_price_max_allowed_deviation = IntegerField(null=True)
    revise_update_price_max_allowed_deviation_mode = IntegerField()
    revise_update_qty = IntegerField()
    revise_update_qty_max_applied_value = IntegerField(null=True)
    revise_update_qty_max_applied_value_mode = IntegerField()
    revise_update_sub_title = IntegerField()
    revise_update_title = IntegerField()
    schedule_interval_settings = TextField(null=True)
    schedule_mode = IntegerField()
    schedule_week_settings = TextField(null=True)
    stop_out_off_stock = IntegerField()
    stop_qty_calculated = IntegerField()
    stop_qty_calculated_value = IntegerField()
    stop_qty_calculated_value_max = IntegerField()
    stop_qty_magento = IntegerField()
    stop_qty_magento_value = IntegerField()
    stop_qty_magento_value_max = IntegerField()
    stop_status_disabled = IntegerField()
    template_synchronization_id = AutoField()

    class Meta:
        table_name = 'm2epro_ebay_template_synchronization'

class M2EproListing(BaseModel):
    account_id = IntegerField(index=True)
    additional_data = TextField(null=True)
    auto_global_adding_add_not_visible = IntegerField(constraints=[SQL("DEFAULT 1")])
    auto_global_adding_mode = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    auto_mode = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    auto_website_adding_add_not_visible = IntegerField(constraints=[SQL("DEFAULT 1")])
    auto_website_adding_mode = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    auto_website_deleting_mode = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    items_active_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    marketplace_id = IntegerField(index=True)
    products_active_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    products_inactive_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    products_total_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    source_products = IntegerField(constraints=[SQL("DEFAULT 1")])
    store_id = IntegerField(index=True)
    title = CharField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_listing'

class M2EproListingAutoCategory(BaseModel):
    category_id = IntegerField(index=True)
    create_date = DateTimeField(null=True)
    group_id = IntegerField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_listing_auto_category'

class M2EproListingAutoCategoryGroup(BaseModel):
    adding_add_not_visible = IntegerField(constraints=[SQL("DEFAULT 1")])
    adding_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    deleting_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    listing_id = IntegerField(index=True)
    title = CharField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_listing_auto_category_group'

class M2EproListingLog(BaseModel):
    action = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    action_id = IntegerField(index=True, null=True)
    additional_data = TextField(null=True)
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    description = TextField(null=True)
    initiator = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    listing_id = IntegerField(index=True, null=True)
    listing_product_id = IntegerField(index=True, null=True)
    listing_title = CharField(index=True, null=True)
    parent_listing_product_id = IntegerField(index=True, null=True)
    priority = IntegerField(constraints=[SQL("DEFAULT 3")], index=True)
    product_id = IntegerField(index=True, null=True)
    product_title = CharField(index=True, null=True)
    type = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_listing_log'

class M2EproListingOther(BaseModel):
    account_id = IntegerField(index=True)
    additional_data = TextField(null=True)
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    marketplace_id = IntegerField(index=True)
    product_id = IntegerField(index=True, null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    status_changer = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_listing_other'

class M2EproListingOtherLog(BaseModel):
    action = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    action_id = IntegerField(index=True, null=True)
    additional_data = TextField(null=True)
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    description = TextField(null=True)
    identifier = CharField(index=True, null=True)
    initiator = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    listing_other_id = IntegerField(index=True, null=True)
    priority = IntegerField(constraints=[SQL("DEFAULT 3")], index=True)
    title = CharField(index=True, null=True)
    type = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_listing_other_log'

class M2EproListingProduct(BaseModel):
    additional_data = TextField(null=True)
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    listing_id = IntegerField(index=True)
    product_id = IntegerField(index=True)
    status = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    status_changer = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    synch_reasons = TextField(null=True)
    synch_status = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    tried_to_list = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_listing_product'

class M2EproListingProductVariation(BaseModel):
    additional_data = TextField(null=True)
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    listing_product_id = IntegerField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_listing_product_variation'

class M2EproListingProductVariationOption(BaseModel):
    attribute = CharField(index=True)
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    listing_product_variation_id = IntegerField(index=True)
    option = CharField(index=True)
    product_id = IntegerField(index=True, null=True)
    product_type = CharField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_listing_product_variation_option'

class M2EproLockItem(BaseModel):
    create_date = DateTimeField(null=True)
    data = TextField(null=True)
    kill_now = IntegerField(constraints=[SQL("DEFAULT 0")])
    nick = CharField(index=True)
    parent_id = IntegerField(index=True, null=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_lock_item'

class M2EproLockedObject(BaseModel):
    create_date = DateTimeField(null=True)
    description = CharField(null=True)
    model_name = CharField(index=True)
    object_id = IntegerField(index=True)
    related_hash = CharField(index=True, null=True)
    tag = CharField(index=True, null=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_locked_object'

class M2EproMarketplace(BaseModel):
    code = CharField()
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    group_title = CharField()
    native_id = IntegerField()
    sorder = IntegerField(constraints=[SQL("DEFAULT 0")])
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    title = CharField()
    update_date = DateTimeField(null=True)
    url = CharField()

    class Meta:
        table_name = 'm2epro_marketplace'

class M2EproMigrationV6(BaseModel):
    component = CharField()
    data = TextField(null=True)
    group = CharField(index=True)

    class Meta:
        table_name = 'm2epro_migration_v6'

class M2EproOperationHistory(BaseModel):
    create_date = DateTimeField(null=True)
    data = TextField(null=True)
    end_date = DateTimeField(index=True, null=True)
    initiator = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    nick = CharField(index=True)
    parent_id = IntegerField(index=True, null=True)
    start_date = DateTimeField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_operation_history'

class M2EproOrder(BaseModel):
    account_id = IntegerField(index=True)
    additional_data = TextField(null=True)
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    magento_order_id = IntegerField(index=True, null=True)
    marketplace_id = IntegerField(index=True, null=True)
    reservation_start_date = DateTimeField(null=True)
    reservation_state = IntegerField(constraints=[SQL("DEFAULT 0")], index=True, null=True)
    store_id = IntegerField(null=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_order'

class M2EproOrderChange(BaseModel):
    action = CharField(index=True)
    component = CharField()
    create_date = DateTimeField(null=True)
    creator_type = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    hash = CharField(index=True, null=True)
    order_id = IntegerField(index=True)
    params = TextField()
    processing_attempt_count = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    processing_attempt_date = DateTimeField(null=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_order_change'

class M2EproOrderItem(BaseModel):
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    order_id = IntegerField(index=True)
    product_details = TextField(null=True)
    product_id = IntegerField(index=True, null=True)
    qty_reserved = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_order_item'

class M2EproOrderLog(BaseModel):
    additional_data = TextField(null=True)
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    description = TextField(null=True)
    initiator = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    order_id = IntegerField(index=True, null=True)
    type = IntegerField(constraints=[SQL("DEFAULT 2")], index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_order_log'

class M2EproOrderMatching(BaseModel):
    component = CharField(index=True)
    create_date = DateTimeField(null=True)
    hash = CharField(index=True, null=True)
    input_variation_options = TextField(null=True)
    output_variation_options = TextField(null=True)
    product_id = IntegerField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_order_matching'

class M2EproPrimaryConfig(BaseModel):
    create_date = DateTimeField(null=True)
    group = CharField(index=True, null=True)
    key = CharField(index=True)
    notice = TextField(null=True)
    update_date = DateTimeField(null=True)
    value = CharField(index=True, null=True)

    class Meta:
        table_name = 'm2epro_primary_config'

class M2EproProcessingRequest(BaseModel):
    component = CharField(index=True)
    create_date = DateTimeField(null=True)
    expiration_date = DateTimeField()
    hash = CharField(index=True)
    next_part = IntegerField(index=True, null=True)
    perform_type = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    processing_hash = CharField(index=True)
    request_body = TextField()
    responser_model = CharField(index=True)
    responser_params = TextField()
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_processing_request'

class M2EproProductChange(BaseModel):
    action = CharField(index=True)
    attribute = CharField(index=True, null=True)
    count_changes = IntegerField(null=True)
    create_date = DateTimeField(null=True)
    initiators = CharField(index=True)
    product_id = IntegerField(index=True)
    store_id = IntegerField(index=True, null=True)
    update_date = DateTimeField(null=True)
    value_new = TextField(null=True)
    value_old = TextField(null=True)

    class Meta:
        table_name = 'm2epro_product_change'

class M2EproRegistry(BaseModel):
    create_date = DateTimeField(null=True)
    key = CharField(index=True)
    update_date = DateTimeField(null=True)
    value = TextField(null=True)

    class Meta:
        table_name = 'm2epro_registry'

class M2EproStopQueue(BaseModel):
    account_hash = CharField(index=True)
    component_mode = CharField(index=True)
    create_date = DateTimeField(null=True)
    is_processed = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    item_data = TextField()
    marketplace_id = IntegerField(index=True, null=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_stop_queue'

class M2EproSynchronizationConfig(BaseModel):
    create_date = DateTimeField(null=True)
    group = CharField(index=True, null=True)
    key = CharField(index=True)
    notice = TextField(null=True)
    update_date = DateTimeField(null=True)
    value = CharField(index=True, null=True)

    class Meta:
        table_name = 'm2epro_synchronization_config'

class M2EproSynchronizationLog(BaseModel):
    additional_data = TextField(null=True)
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    description = TextField(null=True)
    initiator = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    operation_history_id = IntegerField(index=True, null=True)
    priority = IntegerField(constraints=[SQL("DEFAULT 3")], index=True)
    task = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    type = IntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_synchronization_log'

class M2EproSystemLog(BaseModel):
    additional_data = TextField(null=True)
    create_date = DateTimeField(null=True)
    description = TextField(null=True)
    type = CharField(index=True, null=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_system_log'

class M2EproTemplateDescription(BaseModel):
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    title = CharField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_template_description'

class M2EproTemplateSellingFormat(BaseModel):
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    title = CharField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_template_selling_format'

class M2EproTemplateSynchronization(BaseModel):
    component_mode = CharField(index=True, null=True)
    create_date = DateTimeField(null=True)
    revise_change_listing = IntegerField(index=True)
    revise_change_selling_format_template = IntegerField(index=True)
    title = CharField(index=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'm2epro_template_synchronization'

class M2EproWizard(BaseModel):
    nick = CharField(index=True)
    priority = IntegerField()
    status = IntegerField()
    step = CharField(null=True)
    type = IntegerField()
    view = CharField()

    class Meta:
        table_name = 'm2epro_wizard'

class MagemonkeyApiDebug(BaseModel):
    debug_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], index=True)
    debug_id = AutoField()
    request_body = TextField(null=True)
    response_body = TextField(null=True)

    class Meta:
        table_name = 'magemonkey_api_debug'

class MagemonkeyAsyncOrders(BaseModel):
    created_at = DateTimeField()
    info = TextField()
    processed = IntegerField(null=True)

    class Meta:
        table_name = 'magemonkey_async_orders'

class MagemonkeyAsyncSubscribers(BaseModel):
    confirm = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    created_at = DateTimeField()
    email = CharField(null=True)
    lists = TextField()
    mapfields = TextField(null=True)
    order_id = IntegerField(null=True)
    processed = IntegerField(null=True)

    class Meta:
        table_name = 'magemonkey_async_subscribers'

class MagemonkeyAsyncWebhooks(BaseModel):
    processed = IntegerField(constraints=[SQL("DEFAULT 0")])
    webhook_data = TextField(null=True)
    webhook_type = CharField(null=True)

    class Meta:
        table_name = 'magemonkey_async_webhooks'

class MagemonkeyBulksyncExport(BaseModel):
    created_at = DateTimeField()
    data_source_entity = CharField()
    last_processed_id = IntegerField()
    lists = TextField()
    processed_count = IntegerField()
    started_at = DateTimeField(null=True)
    status = CharField(index=True)
    store_id = IntegerField(null=True)
    total_count = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'magemonkey_bulksync_export'

class MagemonkeyBulksyncImport(BaseModel):
    create_customer = IntegerField()
    created_at = DateTimeField()
    import_types = TextField()
    last_processed_id = IntegerField()
    lists = TextField()
    processed_count = IntegerField()
    since = DateTimeField(null=True)
    started_at = DateTimeField(null=True)
    status = CharField(index=True)
    store_id = IntegerField(null=True)
    total_count = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'magemonkey_bulksync_import'

class MagemonkeyEcommerce360(BaseModel):
    created_at = DateTimeField()
    mc_campaign_id = CharField(constraints=[SQL("DEFAULT ''")])
    mc_email_id = CharField(constraints=[SQL("DEFAULT ''")])
    order_id = IntegerField()
    order_increment_id = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    store_id = IntegerField(null=True)

    class Meta:
        table_name = 'magemonkey_ecommerce360'

class MagemonkeyLastOrder(BaseModel):
    date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    email = CharField(null=True)

    class Meta:
        table_name = 'magemonkey_last_order'

class MagemonkeyMailsSent(BaseModel):
    coupon_amount = DecimalField(null=True)
    coupon_number = CharField(null=True)
    coupon_type = IntegerField(null=True)
    customer_email = CharField(null=True)
    customer_name = CharField(null=True)
    mail_type = CharField()
    sent_at = DateTimeField()
    store_id = IntegerField(null=True)

    class Meta:
        table_name = 'magemonkey_mails_sent'

class Magenotification(BaseModel):
    added_date = DateTimeField()
    description = TextField(null=True)
    is_read = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    is_remove = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    magenotification_id = AutoField()
    related_extensions = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    severity = IntegerField(constraints=[SQL("DEFAULT 0")])
    title = CharField()
    url = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'magenotification'

class MagenotificationExtensionFeedback(BaseModel):
    code = CharField(constraints=[SQL("DEFAULT ''")])
    comment = TextField()
    content = TextField()
    coupon_code = CharField(constraints=[SQL("DEFAULT ''")])
    coupon_value = CharField(constraints=[SQL("DEFAULT ''")])
    created = DateTimeField()
    expired_counpon = DateTimeField()
    extension = CharField(constraints=[SQL("DEFAULT ''")])
    extension_version = CharField(constraints=[SQL("DEFAULT ''")])
    feedback_id = AutoField()
    file = TextField()
    is_sent = IntegerField(constraints=[SQL("DEFAULT 2")])
    latest_message = TextField()
    latest_response = TextField()
    latest_response_time = DateTimeField(null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 3")])
    updated = DateTimeField()

    class Meta:
        table_name = 'magenotification_extension_feedback'

class MagenotificationExtensionFeedbackmessage(BaseModel):
    feedback_code = CharField(constraints=[SQL("DEFAULT ''")])
    feedback_id = IntegerField()
    feedbackmessage_id = AutoField()
    file = TextField()
    is_customer = IntegerField(constraints=[SQL("DEFAULT 2")], null=True)
    is_sent = IntegerField(constraints=[SQL("DEFAULT 2")], null=True)
    message = TextField()
    posted_time = DateTimeField(null=True)
    user = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'magenotification_extension_feedbackmessage'

class MagenotificationLicense(BaseModel):
    active_at = DateField()
    domains = CharField(null=True)
    extension_code = CharField(constraints=[SQL("DEFAULT ''")])
    is_valid = IntegerField(null=True)
    license_id = AutoField()
    license_key = TextField()
    response_code = IntegerField(null=True)
    sum_code = CharField(null=True)

    class Meta:
        table_name = 'magenotification_license'

class MagenotificationLog(BaseModel):
    check_date = DateField()
    expired_time = CharField(null=True)
    extension_code = CharField(constraints=[SQL("DEFAULT ''")])
    is_valid = IntegerField(null=True)
    license_key = TextField()
    license_type = CharField(constraints=[SQL("DEFAULT ''")])
    log_id = AutoField()
    response_code = IntegerField(null=True)
    sum_code = CharField(null=True)

    class Meta:
        table_name = 'magenotification_log'

class Magiczoom(BaseModel):
    custom_settings_title = CharField(constraints=[SQL("DEFAULT ''")])
    group_id = IntegerField(null=True)
    last_edit_time = DateTimeField(null=True)
    package = CharField(constraints=[SQL("DEFAULT ''")])
    setting_id = AutoField()
    store_id = IntegerField(null=True)
    theme = CharField(constraints=[SQL("DEFAULT ''")])
    value = TextField(null=True)
    website_id = IntegerField(null=True)

    class Meta:
        table_name = 'magiczoom'

class MailchimpEcommerceSyncData(BaseModel):
    batch_id = CharField(index=True, null=True)
    mailchimp_store_id = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    mailchimp_sync_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    mailchimp_sync_delta = DateTimeField()
    mailchimp_sync_error = CharField(constraints=[SQL("DEFAULT ''")])
    mailchimp_sync_modified = IntegerField(constraints=[SQL("DEFAULT 0")])
    mailchimp_token = CharField(constraints=[SQL("DEFAULT ''")])
    related_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True, null=True)
    type = CharField()

    class Meta:
        table_name = 'mailchimp_ecommerce_sync_data'

class MailchimpErrors(BaseModel):
    batch_id = CharField(constraints=[SQL("DEFAULT '0'")])
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    errors = TextField(null=True)
    mailchimp_store_id = CharField(constraints=[SQL("DEFAULT ''")])
    original_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    regtype = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    store_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    title = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type = CharField(constraints=[SQL("DEFAULT ''")], null=True)

    class Meta:
        table_name = 'mailchimp_errors'

class MailchimpSyncBatches(BaseModel):
    batch_id = CharField()
    status = CharField()
    store_id = CharField()

    class Meta:
        table_name = 'mailchimp_sync_batches'

class MailchimpWebhookRequest(BaseModel):
    data_request = CharField(null=True)
    fired_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    processed = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField()

    class Meta:
        table_name = 'mailchimp_webhook_request'

class MybuysJob(BaseModel):
    dependent_on_job_id = IntegerField(null=True)
    ended_at = DateTimeField(null=True)
    error_message = CharField()
    feed_type = CharField(index=True)
    job_id = AutoField()
    min_entity_id = IntegerField(null=True)
    scheduled_at = DateTimeField(null=True)
    started_at = DateTimeField(null=True)
    status = IntegerField(index=True)
    type = CharField(index=True)
    website_id = IntegerField()

    class Meta:
        table_name = 'mybuys_job'

class NewsletterTemplate(BaseModel):
    added_at = DateTimeField(index=True, null=True)
    modified_at = DateTimeField(index=True, null=True)
    template_actual = IntegerField(constraints=[SQL("DEFAULT 1")], index=True, null=True)
    template_code = CharField(null=True)
    template_id = AutoField()
    template_sender_email = CharField(null=True)
    template_sender_name = CharField(null=True)
    template_styles = TextField(null=True)
    template_subject = CharField(null=True)
    template_text = TextField(null=True)
    template_text_preprocessed = TextField(null=True)
    template_type = IntegerField(null=True)

    class Meta:
        table_name = 'newsletter_template'

class NewsletterQueue(BaseModel):
    newsletter_sender_email = CharField(null=True)
    newsletter_sender_name = CharField(null=True)
    newsletter_styles = TextField(null=True)
    newsletter_subject = CharField(null=True)
    newsletter_text = TextField(null=True)
    newsletter_type = IntegerField(null=True)
    queue_finish_at = DateTimeField(null=True)
    queue_id = AutoField()
    queue_start_at = DateTimeField(null=True)
    queue_status = IntegerField(constraints=[SQL("DEFAULT 0")])
    template = ForeignKeyField(column_name='template_id', constraints=[SQL("DEFAULT 0")], field='template_id', model=NewsletterTemplate)

    class Meta:
        table_name = 'newsletter_queue'

class NewsletterSubscriber(BaseModel):
    change_status_at = DateTimeField(null=True)
    customer_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    mailchimp_sync_delta = DateTimeField()
    mailchimp_sync_error = CharField()
    mailchimp_sync_modified = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore, null=True)
    subscriber_confirm_code = CharField(null=True)
    subscriber_email = CharField(null=True)
    subscriber_firstname = CharField(null=True)
    subscriber_id = AutoField()
    subscriber_lastname = CharField(null=True)
    subscriber_status = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'newsletter_subscriber'

class NewsletterProblem(BaseModel):
    problem_error_code = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    problem_error_text = CharField(null=True)
    problem_id = AutoField()
    queue = ForeignKeyField(column_name='queue_id', constraints=[SQL("DEFAULT 0")], field='queue_id', model=NewsletterQueue)
    subscriber = ForeignKeyField(column_name='subscriber_id', field='subscriber_id', model=NewsletterSubscriber, null=True)

    class Meta:
        table_name = 'newsletter_problem'

class NewsletterQueueLink(BaseModel):
    letter_sent_at = DateTimeField(null=True)
    queue = ForeignKeyField(column_name='queue_id', constraints=[SQL("DEFAULT 0")], field='queue_id', model=NewsletterQueue)
    queue_link_id = AutoField()
    subscriber = ForeignKeyField(column_name='subscriber_id', constraints=[SQL("DEFAULT 0")], field='subscriber_id', model=NewsletterSubscriber)

    class Meta:
        table_name = 'newsletter_queue_link'
        indexes = (
            (('queue', 'letter_sent_at'), False),
        )

class NewsletterQueueStoreLink(BaseModel):
    queue = ForeignKeyField(column_name='queue_id', constraints=[SQL("DEFAULT 0")], field='queue_id', model=NewsletterQueue)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)

    class Meta:
        table_name = 'newsletter_queue_store_link'
        indexes = (
            (('queue', 'store'), True),
        )
        primary_key = CompositeKey('queue', 'store')

class OauthConsumer(BaseModel):
    callback_url = CharField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], index=True)
    entity_id = AutoField()
    key = CharField(unique=True)
    name = CharField()
    rejected_callback_url = CharField()
    secret = CharField(unique=True)
    updated_at = DateTimeField(index=True, null=True)

    class Meta:
        table_name = 'oauth_consumer'

class OauthNonce(BaseModel):
    nonce = CharField(unique=True)
    timestamp = IntegerField()

    class Meta:
        table_name = 'oauth_nonce'
        primary_key = False

class OauthToken(BaseModel):
    admin = ForeignKeyField(column_name='admin_id', field='user_id', model=AdminUser, null=True)
    authorized = IntegerField(constraints=[SQL("DEFAULT 0")])
    callback_url = CharField()
    consumer = ForeignKeyField(column_name='consumer_id', field='entity_id', model=OauthConsumer)
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity, null=True)
    entity_id = AutoField()
    revoked = IntegerField(constraints=[SQL("DEFAULT 0")])
    secret = CharField()
    token = CharField(unique=True)
    type = CharField()
    verifier = CharField(null=True)

    class Meta:
        table_name = 'oauth_token'

class OnestepcheckoutConfigData(BaseModel):
    config_id = AutoField()
    path = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    scope = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    scope_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    value = TextField(null=True)

    class Meta:
        table_name = 'onestepcheckout_config_data'

class OnestepcheckoutDelivery(BaseModel):
    delivery_id = AutoField()
    delivery_security_code = TextField(null=True)
    delivery_time_date = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    order_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'onestepcheckout_delivery'

class OnestepcheckoutSurvey(BaseModel):
    answer = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    order_id = IntegerField()
    question = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    survey_id = AutoField()

    class Meta:
        table_name = 'onestepcheckout_survey'

class PartyPackMatrix(BaseModel):
    ppack_id = AutoField()
    ppack_main_id = IntegerField(null=True)
    product_id = IntegerField(null=True)

    class Meta:
        table_name = 'party_pack_matrix'

class PaypalCert(BaseModel):
    cert_id = AutoField()
    content = TextField(null=True)
    updated_at = DateTimeField(null=True)
    website = ForeignKeyField(column_name='website_id', constraints=[SQL("DEFAULT 0")], field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'paypal_cert'

class PaypalPaymentTransaction(BaseModel):
    additional_information = TextField(null=True)
    created_at = DateTimeField(null=True)
    transaction_id = AutoField()
    txn_id = CharField(null=True, unique=True)

    class Meta:
        table_name = 'paypal_payment_transaction'

class PaypalSettlementReport(BaseModel):
    account_id = CharField(null=True)
    filename = CharField(null=True)
    last_modified = DateTimeField(null=True)
    report_date = DateTimeField(null=True)
    report_id = AutoField()

    class Meta:
        table_name = 'paypal_settlement_report'
        indexes = (
            (('report_date', 'account_id'), True),
        )

class PaypalSettlementReportRow(BaseModel):
    consumer_id = CharField(null=True)
    custom_field = CharField(null=True)
    fee_amount = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    fee_currency = CharField(null=True)
    fee_debit_or_credit = CharField(null=True)
    gross_transaction_amount = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    gross_transaction_currency = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    invoice_id = CharField(null=True)
    payment_tracking_id = CharField(null=True)
    paypal_reference_id = CharField(null=True)
    paypal_reference_id_type = CharField(null=True)
    report = ForeignKeyField(column_name='report_id', field='report_id', model=PaypalSettlementReport)
    row_id = AutoField()
    store_id = CharField(null=True)
    transaction_completion_date = DateTimeField(null=True)
    transaction_debit_or_credit = CharField(constraints=[SQL("DEFAULT 'CR'")])
    transaction_event_code = CharField(null=True)
    transaction_id = CharField(null=True)
    transaction_initiation_date = DateTimeField(null=True)

    class Meta:
        table_name = 'paypal_settlement_report_row'

class PaypalauthCustomer(BaseModel):
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity)
    email = CharField(constraints=[SQL("DEFAULT ''")])
    payer_id = CharField(constraints=[SQL("DEFAULT ''")], unique=True)

    class Meta:
        table_name = 'paypalauth_customer'

class PermissionBlock(BaseModel):
    block_id = AutoField()
    block_name = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    is_allowed = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'permission_block'

class PermissionVariable(BaseModel):
    is_allowed = IntegerField(constraints=[SQL("DEFAULT 0")])
    variable_id = IntegerField()
    variable_name = CharField(constraints=[SQL("DEFAULT ''")], unique=True)

    class Meta:
        table_name = 'permission_variable'
        indexes = (
            (('variable_id', 'variable_name'), True),
        )
        primary_key = CompositeKey('variable_id', 'variable_name')

class PersistentSession(BaseModel):
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity, null=True, unique=True)
    info = TextField(null=True)
    key = CharField(unique=True)
    persistent_id = AutoField()
    updated_at = DateTimeField(index=True, null=True)
    website = ForeignKeyField(column_name='website_id', constraints=[SQL("DEFAULT 0")], field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'persistent_session'

class PickerScheduleDetail(BaseModel):
    created_by = IntegerField(null=True)
    created_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    picker_id = IntegerField(null=True)
    schedule_detail_id = AutoField()
    schedule_id = IntegerField(null=True)
    updated_by = IntegerField(null=True)
    updated_date = DateTimeField(null=True)

    class Meta:
        table_name = 'picker_schedule_detail'

class PmsBatchOrders(BaseModel):
    batch_date = DateTimeField(null=True)
    batch_id = AutoField()
    batch_schedule_id = IntegerField(null=True)
    created_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    order_count = IntegerField(null=True)

    class Meta:
        table_name = 'pms_batch_orders'

class PmsBatchSchedule(BaseModel):
    batch_type = IntegerField(constraints=[SQL("DEFAULT 1")])
    end_hour = TimeField(null=True)
    print_time = TimeField(null=True)
    schedule_id = AutoField()
    schedule_label = CharField(null=True)
    start_hour = TimeField(null=True)

    class Meta:
        table_name = 'pms_batch_schedule'

class PmsOrderBatch(BaseModel):
    batch_id = IntegerField(null=True)
    created_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    order_batch_id = AutoField()

    class Meta:
        table_name = 'pms_order_batch'

class PmsOrders(BaseModel):
    created_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    login_id = IntegerField(null=True)
    order_id = IntegerField(null=True)
    order_number = CharField(null=True)

    class Meta:
        table_name = 'pms_orders'

class PmsPickerLogin(BaseModel):
    actual_picked_orders = IntegerField(null=True)
    admin_login = BooleanField(null=True)  # bit
    login = DateTimeField(null=True)
    login_id = AutoField()
    logout = DateTimeField(null=True)
    picker_id = IntegerField(null=True)
    total_orders = IntegerField(null=True)

    class Meta:
        table_name = 'pms_picker_login'

class PmsPickerSchedule(BaseModel):
    created_by = IntegerField(null=True)
    created_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    date = DateField(null=True)
    hour = IntegerField(null=True)
    number_of_pickers = IntegerField(null=True)
    picker_schedule_id = AutoField()

    class Meta:
        table_name = 'pms_picker_schedule'

class PmsPickerScheduleDetail(BaseModel):
    created_by = IntegerField(null=True)
    created_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    picker_id = IntegerField(null=True)
    schedule_detail_id = AutoField()
    schedule_id = IntegerField(null=True)
    updated_by = IntegerField(null=True)
    updated_date = DateTimeField(null=True)

    class Meta:
        table_name = 'pms_picker_schedule_detail'

class PmsPickerScheduleResults(BaseModel):
    batch_id = IntegerField(null=True)
    orders_completed = IntegerField(null=True)
    orders_notcompleted = IntegerField(null=True)
    picker_id = IntegerField(null=True)
    results_id = AutoField()
    schedule_detail_id = IntegerField(null=True)
    time_completed = TimeField(null=True)
    time_started = TimeField(null=True)

    class Meta:
        table_name = 'pms_picker_schedule_results'

class PmsPickers(BaseModel):
    created_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    email = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    password = CharField(null=True)
    picker_code = CharField(null=True)
    picker_id = AutoField()
    pin = CharField(null=True)
    security_level = IntegerField(null=True)

    class Meta:
        table_name = 'pms_pickers'

class PmsSecuritylevel(BaseModel):
    clearance = IntegerField(null=True)
    level_id = AutoField()
    level_name = CharField(null=True)

    class Meta:
        table_name = 'pms_securitylevel'

class Poll(BaseModel):
    active = IntegerField(constraints=[SQL("DEFAULT 1")])
    answers_display = IntegerField(null=True)
    closed = IntegerField(constraints=[SQL("DEFAULT 0")])
    date_closed = DateTimeField(null=True)
    date_posted = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    poll_id = AutoField()
    poll_title = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    votes_count = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'poll'

class PollAnswer(BaseModel):
    answer_id = AutoField()
    answer_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    answer_title = CharField(null=True)
    poll = ForeignKeyField(column_name='poll_id', constraints=[SQL("DEFAULT 0")], field='poll_id', model=Poll)
    votes_count = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'poll_answer'

class PollStore(BaseModel):
    poll = ForeignKeyField(column_name='poll_id', constraints=[SQL("DEFAULT 0")], field='poll_id', model=Poll)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)

    class Meta:
        table_name = 'poll_store'
        indexes = (
            (('poll', 'store'), True),
        )
        primary_key = CompositeKey('poll', 'store')

class PollVote(BaseModel):
    customer_id = IntegerField(null=True)
    ip_address = CharField(null=True)
    poll_answer = ForeignKeyField(column_name='poll_answer_id', constraints=[SQL("DEFAULT 0")], field='answer_id', model=PollAnswer)
    poll_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    vote_id = AutoField()
    vote_time = DateTimeField(null=True)

    class Meta:
        table_name = 'poll_vote'

class ProdAssoc(BaseModel):
    dev_id = IntegerField(column_name='Dev_ID', constraints=[SQL("DEFAULT 0")], null=True)
    live_id = IntegerField(column_name='Live_ID', constraints=[SQL("DEFAULT 0")])
    sku = CharField(null=True)

    class Meta:
        table_name = 'prod_assoc'
        primary_key = False

class ProductAlertPrice(BaseModel):
    add_date = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    alert_price_id = AutoField()
    customer = ForeignKeyField(column_name='customer_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerEntity)
    last_send_date = DateTimeField(null=True)
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    send_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    website = ForeignKeyField(column_name='website_id', constraints=[SQL("DEFAULT 0")], field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'product_alert_price'

class ProductAlertStock(BaseModel):
    add_date = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    alert_stock_id = AutoField()
    customer = ForeignKeyField(column_name='customer_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerEntity)
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    send_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    send_date = DateTimeField(null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    website = ForeignKeyField(column_name='website_id', constraints=[SQL("DEFAULT 0")], field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'product_alert_stock'

class ProductIds(BaseModel):
    live_id = IntegerField(index=True, null=True)
    old_id = IntegerField(index=True, null=True)
    sku = CharField(null=True)

    class Meta:
        table_name = 'product_ids'

class ProductTrend(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    current_week = DecimalField(null=True)
    entity_id = IntegerField(index=True, null=True)
    previous_week = DecimalField(null=True)
    sku = CharField(null=True)
    trend_id = AutoField()

    class Meta:
        table_name = 'product_trend'

class ProfitabilityOrder(BaseModel):
    anomaly = IntegerField()
    order_number = TextField()
    profit = TextField()
    timestamp = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'profitability_order'

class PurchaseOrder(BaseModel):
    created_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    last_edit = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    receipt_date = DateTimeField(null=True)
    reconciled = IntegerField(null=True)
    status = CharField(constraints=[SQL("DEFAULT 'open'")])
    total_cost = DecimalField()
    total_items = IntegerField()
    user = CharField()
    vendor_id = IntegerField()

    class Meta:
        table_name = 'purchase_order'
        indexes = (
            (('status', 'id'), False),
        )

class PurchaseOrderItems(BaseModel):
    cost = DecimalField()
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    line_number = IntegerField()
    po_id = IntegerField()
    qty_received = IntegerField()
    received_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    reconciled_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    sku = CharField()
    status = CharField(constraints=[SQL("DEFAULT 'open'")])
    status_code = IntegerField(constraints=[SQL("DEFAULT 1")])
    vendor_qty = IntegerField()

    class Meta:
        table_name = 'purchase_order_items'
        indexes = (
            (('po_id', 'sku', 'status'), False),
        )

class PurchaseOrderMessage(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    message = CharField()
    po_id = IntegerField(index=True)

    class Meta:
        table_name = 'purchase_order_message'

class PurchaseOrderStatusCode(BaseModel):
    status_description = CharField()
    status_id = AutoField()

    class Meta:
        table_name = 'purchase_order_status_code'

class RatingEntity(BaseModel):
    entity_code = CharField(unique=True)
    entity_id = AutoField()

    class Meta:
        table_name = 'rating_entity'

class Rating(BaseModel):
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=RatingEntity)
    position = IntegerField(constraints=[SQL("DEFAULT 0")])
    rating_code = CharField(unique=True)
    rating_id = AutoField()

    class Meta:
        table_name = 'rating'

class RatingOption(BaseModel):
    code = CharField()
    option_id = AutoField()
    position = IntegerField(constraints=[SQL("DEFAULT 0")])
    rating = ForeignKeyField(column_name='rating_id', constraints=[SQL("DEFAULT 0")], field='rating_id', model=Rating)
    value = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'rating_option'

class RatingOptionVote(BaseModel):
    customer_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    entity_pk_value = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    option = ForeignKeyField(column_name='option_id', constraints=[SQL("DEFAULT 0")], field='option_id', model=RatingOption)
    percent = IntegerField(constraints=[SQL("DEFAULT 0")])
    rating_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    remote_ip = CharField(null=True)
    remote_ip_long = CharField(null=True)
    review = ForeignKeyField(column_name='review_id', field='review_id', model=Review, null=True)
    value = IntegerField(constraints=[SQL("DEFAULT 0")])
    vote_id = BigAutoField()

    class Meta:
        table_name = 'rating_option_vote'

class RatingOptionVoteAggregated(BaseModel):
    entity_pk_value = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    percent = IntegerField(constraints=[SQL("DEFAULT 0")])
    percent_approved = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    primary_id = AutoField()
    rating = ForeignKeyField(column_name='rating_id', constraints=[SQL("DEFAULT 0")], field='rating_id', model=Rating)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    vote_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    vote_value_sum = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'rating_option_vote_aggregated'

class RatingStore(BaseModel):
    rating = ForeignKeyField(column_name='rating_id', constraints=[SQL("DEFAULT 0")], field='rating_id', model=Rating)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)

    class Meta:
        table_name = 'rating_store'
        indexes = (
            (('rating', 'store'), True),
        )
        primary_key = CompositeKey('rating', 'store')

class RatingTitle(BaseModel):
    rating = ForeignKeyField(column_name='rating_id', constraints=[SQL("DEFAULT 0")], field='rating_id', model=Rating)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    value = CharField()

    class Meta:
        table_name = 'rating_title'
        indexes = (
            (('rating', 'store'), True),
        )
        primary_key = CompositeKey('rating', 'store')

class ReportComparedProductIndex(BaseModel):
    added_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")], index=True)
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity, null=True)
    index_id = BigAutoField()
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    visitor_id = IntegerField(null=True)

    class Meta:
        table_name = 'report_compared_product_index'
        indexes = (
            (('customer', 'product'), True),
            (('visitor_id', 'product'), True),
        )

class ReportEventTypes(BaseModel):
    customer_login = IntegerField(constraints=[SQL("DEFAULT 0")])
    event_name = CharField()
    event_type_id = AutoField()

    class Meta:
        table_name = 'report_event_types'

class ReportEvent(BaseModel):
    event_id = BigAutoField()
    event_type = ForeignKeyField(column_name='event_type_id', constraints=[SQL("DEFAULT 0")], field='event_type_id', model=ReportEventTypes)
    logged_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    object_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore)
    subject_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    subtype = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'report_event'

class ReportViewedProductAggregatedDaily(BaseModel):
    period = DateField(null=True)
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity, null=True)
    product_name = CharField(null=True)
    product_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    rating_pos = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    views_num = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'report_viewed_product_aggregated_daily'
        indexes = (
            (('period', 'store', 'product'), True),
        )

class ReportViewedProductAggregatedMonthly(BaseModel):
    period = DateField(null=True)
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity, null=True)
    product_name = CharField(null=True)
    product_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    rating_pos = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    views_num = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'report_viewed_product_aggregated_monthly'
        indexes = (
            (('period', 'store', 'product'), True),
        )

class ReportViewedProductAggregatedYearly(BaseModel):
    period = DateField(null=True)
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity, null=True)
    product_name = CharField(null=True)
    product_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    rating_pos = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    views_num = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'report_viewed_product_aggregated_yearly'
        indexes = (
            (('period', 'store', 'product'), True),
        )

class ReportViewedProductIndex(BaseModel):
    added_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")], index=True)
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity, null=True)
    index_id = BigAutoField()
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    visitor_id = IntegerField(null=True)

    class Meta:
        table_name = 'report_viewed_product_index'
        indexes = (
            (('customer', 'product'), True),
            (('visitor_id', 'product'), True),
        )

class ReportingCounts(BaseModel):
    count = IntegerField(null=True)
    entity_id = AutoField()
    type = CharField(null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'reporting_counts'

class ReportingModuleStatus(BaseModel):
    active = CharField(null=True)
    codepool = CharField(null=True)
    entity_id = AutoField()
    name = CharField(null=True)
    state = CharField(null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    version = CharField(null=True)

    class Meta:
        table_name = 'reporting_module_status'

class ReportingOrders(BaseModel):
    customer_id = IntegerField(null=True)
    entity_id = AutoField()
    item_count = IntegerField()
    total = DecimalField(null=True)
    total_base = DecimalField(null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'reporting_orders'

class ReportingSystemUpdates(BaseModel):
    action = CharField(null=True)
    entity_id = AutoField()
    type = CharField(null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'reporting_system_updates'

class ReportingUsers(BaseModel):
    action = CharField(null=True)
    entity_id = AutoField()
    type = CharField(null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'reporting_users'

class ReviewDetail(BaseModel):
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity, null=True)
    detail = TextField()
    detail_id = BigAutoField()
    nickname = CharField()
    review = ForeignKeyField(column_name='review_id', constraints=[SQL("DEFAULT 0")], field='review_id', model=Review)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore, null=True)
    title = CharField()

    class Meta:
        table_name = 'review_detail'

class ReviewEntitySummary(BaseModel):
    entity_pk_value = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    entity_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    primary_id = BigAutoField()
    rating_summary = IntegerField(constraints=[SQL("DEFAULT 0")])
    reviews_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)

    class Meta:
        table_name = 'review_entity_summary'

class ReviewStore(BaseModel):
    review = ForeignKeyField(column_name='review_id', field='review_id', model=Review)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore)

    class Meta:
        table_name = 'review_store'
        indexes = (
            (('review', 'store'), True),
        )
        primary_key = CompositeKey('review', 'store')

class SalesBestsellersAggregatedDaily(BaseModel):
    period = DateField(null=True)
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity, null=True)
    product_name = CharField(null=True)
    product_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    product_type_id = CharField(constraints=[SQL("DEFAULT 'simple'")])
    qty_ordered = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    rating_pos = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)

    class Meta:
        table_name = 'sales_bestsellers_aggregated_daily'
        indexes = (
            (('period', 'store', 'product'), True),
        )

class SalesBestsellersAggregatedMonthly(BaseModel):
    period = DateField(null=True)
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity, null=True)
    product_name = CharField(null=True)
    product_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    product_type_id = CharField(constraints=[SQL("DEFAULT 'simple'")])
    qty_ordered = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    rating_pos = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)

    class Meta:
        table_name = 'sales_bestsellers_aggregated_monthly'
        indexes = (
            (('period', 'store', 'product'), True),
        )

class SalesBestsellersAggregatedYearly(BaseModel):
    period = DateField(null=True)
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity, null=True)
    product_name = CharField(null=True)
    product_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    product_type_id = CharField(constraints=[SQL("DEFAULT 'simple'")])
    qty_ordered = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    rating_pos = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)

    class Meta:
        table_name = 'sales_bestsellers_aggregated_yearly'
        indexes = (
            (('period', 'store', 'product'), True),
        )

class SalesBillingAgreement(BaseModel):
    agreement_id = AutoField()
    agreement_label = CharField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity)
    method_code = CharField()
    reference_id = CharField()
    status = CharField()
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'sales_billing_agreement'

class SalesBillingAgreementOrder(BaseModel):
    agreement = ForeignKeyField(column_name='agreement_id', field='agreement_id', model=SalesBillingAgreement)
    order = ForeignKeyField(column_name='order_id', field='entity_id', model=SalesFlatOrder)

    class Meta:
        table_name = 'sales_billing_agreement_order'
        indexes = (
            (('agreement', 'order'), True),
        )
        primary_key = CompositeKey('agreement', 'order')

class SalesData(BaseModel):
    created_at = DateTimeField(null=True)
    increment_id = CharField(null=True)
    order_id = IntegerField(null=True)
    product_id = IntegerField(null=True)
    qty_ordered = DecimalField(null=True)
    sku = CharField(null=True)

    class Meta:
        table_name = 'sales_data'

class SalesDataOrder(BaseModel):
    base_shipping_amount = DecimalField(null=True)
    created_at = DateTimeField(null=True)
    entity_id = IntegerField(null=True)
    increment_id = CharField(null=True)
    subtotal = DecimalField(null=True)
    total_item_count = IntegerField(null=True)

    class Meta:
        table_name = 'sales_data_order'

class SalesFlatCreditmemo(BaseModel):
    adjustment = DecimalField(null=True)
    adjustment_negative = DecimalField(null=True)
    adjustment_positive = DecimalField(null=True)
    base_adjustment = DecimalField(null=True)
    base_adjustment_negative = DecimalField(null=True)
    base_adjustment_positive = DecimalField(null=True)
    base_currency_code = CharField(null=True)
    base_discount_amount = DecimalField(null=True)
    base_grand_total = DecimalField(null=True)
    base_hidden_tax_amount = DecimalField(null=True)
    base_shipping_amount = DecimalField(null=True)
    base_shipping_hidden_tax_amnt = DecimalField(null=True)
    base_shipping_incl_tax = DecimalField(null=True)
    base_shipping_tax_amount = DecimalField(null=True)
    base_subtotal = DecimalField(null=True)
    base_subtotal_incl_tax = DecimalField(null=True)
    base_tax_amount = DecimalField(null=True)
    base_to_global_rate = DecimalField(null=True)
    base_to_order_rate = DecimalField(null=True)
    billing_address_id = IntegerField(null=True)
    created_at = DateTimeField(index=True, null=True)
    creditmemo_status = IntegerField(index=True, null=True)
    discount_amount = DecimalField(null=True)
    discount_description = CharField(null=True)
    email_sent = IntegerField(null=True)
    entity_id = AutoField()
    global_currency_code = CharField(null=True)
    grand_total = DecimalField(null=True)
    hidden_tax_amount = DecimalField(null=True)
    increment_id = CharField(null=True, unique=True)
    invoice_id = IntegerField(null=True)
    order_currency_code = CharField(null=True)
    order = ForeignKeyField(column_name='order_id', field='entity_id', model=SalesFlatOrder)
    shipping_address_id = IntegerField(null=True)
    shipping_amount = DecimalField(null=True)
    shipping_hidden_tax_amount = DecimalField(null=True)
    shipping_incl_tax = DecimalField(null=True)
    shipping_tax_amount = DecimalField(null=True)
    state = IntegerField(index=True, null=True)
    store_currency_code = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    store_to_base_rate = DecimalField(null=True)
    store_to_order_rate = DecimalField(null=True)
    subtotal = DecimalField(null=True)
    subtotal_incl_tax = DecimalField(null=True)
    tax_amount = DecimalField(null=True)
    transaction_id = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'sales_flat_creditmemo'

class SalesFlatCreditmemoComment(BaseModel):
    comment = TextField(null=True)
    created_at = DateTimeField(index=True, null=True)
    entity_id = AutoField()
    is_customer_notified = IntegerField(null=True)
    is_visible_on_front = IntegerField(constraints=[SQL("DEFAULT 0")])
    parent = ForeignKeyField(column_name='parent_id', field='entity_id', model=SalesFlatCreditmemo)

    class Meta:
        table_name = 'sales_flat_creditmemo_comment'

class SalesFlatCreditmemoGrid(BaseModel):
    base_currency_code = CharField(null=True)
    base_grand_total = DecimalField(index=True, null=True)
    base_to_global_rate = DecimalField(null=True)
    base_to_order_rate = DecimalField(null=True)
    billing_name = CharField(index=True, null=True)
    created_at = DateTimeField(index=True, null=True)
    creditmemo_status = IntegerField(index=True, null=True)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=SalesFlatCreditmemo, primary_key=True)
    global_currency_code = CharField(null=True)
    grand_total = DecimalField(index=True, null=True)
    increment_id = CharField(null=True, unique=True)
    invoice_id = IntegerField(null=True)
    order_created_at = DateTimeField(index=True, null=True)
    order_currency_code = CharField(null=True)
    order_id = IntegerField(index=True)
    order_increment_id = CharField(index=True, null=True)
    state = IntegerField(index=True, null=True)
    store_currency_code = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    store_to_base_rate = DecimalField(null=True)
    store_to_order_rate = DecimalField(null=True)

    class Meta:
        table_name = 'sales_flat_creditmemo_grid'

class SalesFlatCreditmemoItem(BaseModel):
    additional_data = TextField(null=True)
    base_cost = DecimalField(null=True)
    base_discount_amount = DecimalField(null=True)
    base_hidden_tax_amount = DecimalField(null=True)
    base_price = DecimalField(null=True)
    base_price_incl_tax = DecimalField(null=True)
    base_row_total = DecimalField(null=True)
    base_row_total_incl_tax = DecimalField(null=True)
    base_tax_amount = DecimalField(null=True)
    base_weee_tax_applied_amount = DecimalField(null=True)
    base_weee_tax_applied_row_amnt = DecimalField(null=True)
    base_weee_tax_disposition = DecimalField(null=True)
    base_weee_tax_row_disposition = DecimalField(null=True)
    description = TextField(null=True)
    discount_amount = DecimalField(null=True)
    entity_id = AutoField()
    hidden_tax_amount = DecimalField(null=True)
    name = CharField(null=True)
    order_item_id = IntegerField(null=True)
    parent = ForeignKeyField(column_name='parent_id', field='entity_id', model=SalesFlatCreditmemo)
    price = DecimalField(null=True)
    price_incl_tax = DecimalField(null=True)
    product_id = IntegerField(null=True)
    qty = DecimalField(null=True)
    row_total = DecimalField(null=True)
    row_total_incl_tax = DecimalField(null=True)
    sku = CharField(null=True)
    tax_amount = DecimalField(null=True)
    weee_tax_applied = TextField(null=True)
    weee_tax_applied_amount = DecimalField(null=True)
    weee_tax_applied_row_amount = DecimalField(null=True)
    weee_tax_disposition = DecimalField(null=True)
    weee_tax_row_disposition = DecimalField(null=True)

    class Meta:
        table_name = 'sales_flat_creditmemo_item'

class SalesFlatInvoice(BaseModel):
    base_currency_code = CharField(null=True)
    base_discount_amount = DecimalField(null=True)
    base_grand_total = DecimalField(null=True)
    base_hidden_tax_amount = DecimalField(null=True)
    base_shipping_amount = DecimalField(null=True)
    base_shipping_hidden_tax_amnt = DecimalField(null=True)
    base_shipping_incl_tax = DecimalField(null=True)
    base_shipping_tax_amount = DecimalField(null=True)
    base_subtotal = DecimalField(null=True)
    base_subtotal_incl_tax = DecimalField(null=True)
    base_tax_amount = DecimalField(null=True)
    base_to_global_rate = DecimalField(null=True)
    base_to_order_rate = DecimalField(null=True)
    base_total_refunded = DecimalField(null=True)
    billing_address_id = IntegerField(null=True)
    can_void_flag = IntegerField(null=True)
    created_at = DateTimeField(index=True, null=True)
    discount_amount = DecimalField(null=True)
    discount_description = CharField(null=True)
    email_sent = IntegerField(null=True)
    entity_id = AutoField()
    global_currency_code = CharField(null=True)
    grand_total = DecimalField(index=True, null=True)
    hidden_tax_amount = DecimalField(null=True)
    increment_id = CharField(null=True, unique=True)
    is_used_for_refund = IntegerField(null=True)
    order_currency_code = CharField(null=True)
    order = ForeignKeyField(column_name='order_id', field='entity_id', model=SalesFlatOrder)
    shipping_address_id = IntegerField(null=True)
    shipping_amount = DecimalField(null=True)
    shipping_hidden_tax_amount = DecimalField(null=True)
    shipping_incl_tax = DecimalField(null=True)
    shipping_tax_amount = DecimalField(null=True)
    state = IntegerField(index=True, null=True)
    store_currency_code = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    store_to_base_rate = DecimalField(null=True)
    store_to_order_rate = DecimalField(null=True)
    subtotal = DecimalField(null=True)
    subtotal_incl_tax = DecimalField(null=True)
    tax_amount = DecimalField(null=True)
    total_qty = DecimalField(null=True)
    transaction_id = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'sales_flat_invoice'

class SalesFlatInvoiceComment(BaseModel):
    comment = TextField(null=True)
    created_at = DateTimeField(index=True, null=True)
    entity_id = AutoField()
    is_customer_notified = IntegerField(null=True)
    is_visible_on_front = IntegerField(constraints=[SQL("DEFAULT 0")])
    parent = ForeignKeyField(column_name='parent_id', field='entity_id', model=SalesFlatInvoice)

    class Meta:
        table_name = 'sales_flat_invoice_comment'

class SalesFlatInvoiceGrid(BaseModel):
    base_currency_code = CharField(null=True)
    base_grand_total = DecimalField(null=True)
    billing_name = CharField(index=True, null=True)
    created_at = DateTimeField(index=True, null=True)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=SalesFlatInvoice, primary_key=True)
    global_currency_code = CharField(null=True)
    grand_total = DecimalField(index=True, null=True)
    increment_id = CharField(null=True, unique=True)
    order_created_at = DateTimeField(index=True, null=True)
    order_currency_code = CharField(null=True)
    order_id = IntegerField(index=True)
    order_increment_id = CharField(index=True, null=True)
    state = IntegerField(index=True, null=True)
    store_currency_code = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)

    class Meta:
        table_name = 'sales_flat_invoice_grid'

class SalesFlatInvoiceItem(BaseModel):
    additional_data = TextField(null=True)
    base_cost = DecimalField(null=True)
    base_discount_amount = DecimalField(null=True)
    base_hidden_tax_amount = DecimalField(null=True)
    base_price = DecimalField(null=True)
    base_price_incl_tax = DecimalField(null=True)
    base_row_total = DecimalField(null=True)
    base_row_total_incl_tax = DecimalField(null=True)
    base_tax_amount = DecimalField(null=True)
    base_weee_tax_applied_amount = DecimalField(null=True)
    base_weee_tax_applied_row_amnt = DecimalField(null=True)
    base_weee_tax_disposition = DecimalField(null=True)
    base_weee_tax_row_disposition = DecimalField(null=True)
    description = TextField(null=True)
    discount_amount = DecimalField(null=True)
    entity_id = AutoField()
    hidden_tax_amount = DecimalField(null=True)
    name = CharField(null=True)
    order_item_id = IntegerField(null=True)
    parent = ForeignKeyField(column_name='parent_id', field='entity_id', model=SalesFlatInvoice)
    price = DecimalField(null=True)
    price_incl_tax = DecimalField(null=True)
    product_id = IntegerField(null=True)
    qty = DecimalField(null=True)
    row_total = DecimalField(null=True)
    row_total_incl_tax = DecimalField(null=True)
    sku = CharField(null=True)
    tax_amount = DecimalField(null=True)
    weee_tax_applied = TextField(null=True)
    weee_tax_applied_amount = DecimalField(null=True)
    weee_tax_applied_row_amount = DecimalField(null=True)
    weee_tax_disposition = DecimalField(null=True)
    weee_tax_row_disposition = DecimalField(null=True)

    class Meta:
        table_name = 'sales_flat_invoice_item'

class SalesFlatOrderAddress(BaseModel):
    address_type = CharField(null=True)
    city = CharField(null=True)
    company = CharField(null=True)
    country_id = CharField(null=True)
    customer_address_id = IntegerField(null=True)
    customer_id = IntegerField(null=True)
    delivery_instruction = TextField(null=True)
    email = CharField(null=True)
    entity_id = AutoField()
    fax = CharField(null=True)
    firstname = CharField(null=True)
    lastname = CharField(null=True)
    middlename = CharField(null=True)
    parent = ForeignKeyField(column_name='parent_id', field='entity_id', model=SalesFlatOrder, null=True)
    party_date = DateTimeField(null=True)
    postcode = CharField(null=True)
    prefix = CharField(null=True)
    quote_address_id = IntegerField(null=True)
    region = CharField(null=True)
    region_id = IntegerField(null=True)
    street = CharField(null=True)
    suffix = CharField(null=True)
    telephone = CharField(null=True)
    vat_id = TextField(null=True)
    vat_is_valid = IntegerField(null=True)
    vat_request_date = TextField(null=True)
    vat_request_id = TextField(null=True)
    vat_request_success = IntegerField(null=True)

    class Meta:
        table_name = 'sales_flat_order_address'

class SalesFlatOrderGrid(BaseModel):
    base_currency_code = CharField(null=True)
    base_grand_total = DecimalField(index=True, null=True)
    base_total_paid = DecimalField(index=True, null=True)
    billing_name = CharField(index=True, null=True)
    created_at = DateTimeField(index=True, null=True)
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity, null=True)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=SalesFlatOrder, primary_key=True)
    grand_total = DecimalField(index=True, null=True)
    increment_id = CharField(null=True, unique=True)
    order_currency_code = CharField(null=True)
    shipping_name = CharField(index=True, null=True)
    status = CharField(index=True, null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    store_name = CharField(null=True)
    total_paid = DecimalField(index=True, null=True)
    updated_at = DateTimeField(index=True, null=True)

    class Meta:
        table_name = 'sales_flat_order_grid'

class SalesFlatOrderPayment(BaseModel):
    account_status = CharField(null=True)
    additional_data = TextField(null=True)
    additional_information = TextField(null=True)
    address_status = CharField(null=True)
    amount_authorized = DecimalField(null=True)
    amount_canceled = DecimalField(null=True)
    amount_ordered = DecimalField(null=True)
    amount_paid = DecimalField(null=True)
    amount_refunded = DecimalField(null=True)
    anet_trans_method = CharField(null=True)
    base_amount_authorized = DecimalField(null=True)
    base_amount_canceled = DecimalField(null=True)
    base_amount_ordered = DecimalField(null=True)
    base_amount_paid = DecimalField(null=True)
    base_amount_paid_online = DecimalField(null=True)
    base_amount_refunded = DecimalField(null=True)
    base_amount_refunded_online = DecimalField(null=True)
    base_shipping_amount = DecimalField(null=True)
    base_shipping_captured = DecimalField(null=True)
    base_shipping_refunded = DecimalField(null=True)
    cc_approval = CharField(null=True)
    cc_avs_status = CharField(null=True)
    cc_cid_status = CharField(null=True)
    cc_debug_request_body = CharField(null=True)
    cc_debug_response_body = CharField(null=True)
    cc_debug_response_serialized = CharField(null=True)
    cc_exp_month = CharField(null=True)
    cc_exp_year = CharField(null=True)
    cc_last4 = CharField(null=True)
    cc_number_enc = CharField(null=True)
    cc_owner = CharField(null=True)
    cc_secure_verify = CharField(null=True)
    cc_ss_issue = CharField(null=True)
    cc_ss_start_month = CharField(null=True)
    cc_ss_start_year = CharField(null=True)
    cc_status = CharField(null=True)
    cc_status_description = CharField(null=True)
    cc_trans_id = CharField(null=True)
    cc_type = CharField(null=True)
    echeck_account_name = CharField(null=True)
    echeck_account_type = CharField(null=True)
    echeck_bank_name = CharField(null=True)
    echeck_routing_number = CharField(null=True)
    echeck_type = CharField(null=True)
    entity_id = AutoField()
    last_trans_id = CharField(null=True)
    method = CharField(null=True)
    parent = ForeignKeyField(column_name='parent_id', field='entity_id', model=SalesFlatOrder)
    paybox_request_number = CharField(null=True)
    po_number = CharField(null=True)
    protection_eligibility = CharField(null=True)
    quote_payment_id = IntegerField(null=True)
    shipping_amount = DecimalField(null=True)
    shipping_captured = DecimalField(null=True)
    shipping_refunded = DecimalField(null=True)

    class Meta:
        table_name = 'sales_flat_order_payment'

class SalesFlatOrderStatusHistory(BaseModel):
    comment = TextField(null=True)
    created_at = DateTimeField(index=True, null=True)
    entity_id = AutoField()
    entity_name = CharField(null=True)
    is_customer_notified = IntegerField(null=True)
    is_visible_on_front = IntegerField(constraints=[SQL("DEFAULT 0")])
    parent = ForeignKeyField(column_name='parent_id', field='entity_id', model=SalesFlatOrder)
    status = CharField(null=True)

    class Meta:
        table_name = 'sales_flat_order_status_history'

class SalesFlatQuote(BaseModel):
    applied_rule_ids = CharField(null=True)
    auctaneapi_discounts = TextField(null=True)
    base_currency_code = CharField(null=True)
    base_grand_total = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    base_subtotal = DecimalField(null=True)
    base_subtotal_with_discount = DecimalField(null=True)
    base_to_global_rate = DecimalField(null=True)
    base_to_quote_rate = DecimalField(null=True)
    checkout_method = CharField(null=True)
    comments = TextField(null=True)
    converted_at = DateTimeField(null=True)
    coupon_code = CharField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    customer_dob = DateTimeField(null=True)
    customer_email = CharField(null=True)
    customer_firstname = CharField(null=True)
    customer_gender = CharField(null=True)
    customer_group_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    customer_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    customer_is_guest = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    customer_lastname = CharField(null=True)
    customer_middlename = CharField(null=True)
    customer_note = CharField(null=True)
    customer_note_notify = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    customer_prefix = CharField(null=True)
    customer_suffix = CharField(null=True)
    customer_tax_class_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    customer_taxvat = CharField(null=True)
    ebizmarts_abandonedcart_counter = IntegerField(constraints=[SQL("DEFAULT 0")])
    ebizmarts_abandonedcart_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    ebizmarts_abandonedcart_token = CharField(null=True)
    entity_id = AutoField()
    ext_shipping_info = TextField(null=True)
    gift_message_id = IntegerField(null=True)
    global_currency_code = CharField(null=True)
    grand_total = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    is_changed = IntegerField(null=True)
    is_multi_shipping = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    is_persistent = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    is_virtual = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    items_count = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    items_qty = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    mailchimp_abandonedcart_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    mailchimp_campaign_id = CharField(constraints=[SQL("DEFAULT ''")])
    mailchimp_landing_page = CharField(constraints=[SQL("DEFAULT ''")])
    orig_order_id = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    party_date = DateTimeField(null=True)
    password_hash = CharField(null=True)
    quote_currency_code = CharField(null=True)
    remote_ip = CharField(null=True)
    reserved_order_id = CharField(null=True)
    shipping_pobox = IntegerField(null=True)
    store_currency_code = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    store_to_base_rate = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    store_to_quote_rate = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    subtotal = DecimalField(null=True)
    subtotal_with_discount = DecimalField(null=True)
    trigger_recollect = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])

    class Meta:
        table_name = 'sales_flat_quote'
        indexes = (
            (('customer_id', 'store', 'is_active'), False),
        )

class SalesFlatQuoteAddress(BaseModel):
    address_id = AutoField()
    address_type = CharField(null=True)
    applied_taxes = TextField(null=True)
    base_discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    base_grand_total = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    base_hidden_tax_amount = DecimalField(null=True)
    base_shipping_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    base_shipping_discount_amount = DecimalField(null=True)
    base_shipping_hidden_tax_amnt = DecimalField(null=True)
    base_shipping_incl_tax = DecimalField(null=True)
    base_shipping_tax_amount = DecimalField(null=True)
    base_subtotal = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    base_subtotal_total_incl_tax = DecimalField(null=True)
    base_subtotal_with_discount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    base_tax_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    city = CharField(null=True)
    collect_shipping_rates = IntegerField(constraints=[SQL("DEFAULT 0")])
    company = CharField(null=True)
    country_id = CharField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    customer_address_id = IntegerField(null=True)
    customer_id = IntegerField(null=True)
    customer_notes = TextField(null=True)
    delivery_instruction = TextField(null=True)
    discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    discount_description = CharField(null=True)
    email = CharField(null=True)
    fax = CharField(null=True)
    firstname = CharField(null=True)
    free_shipping = IntegerField(constraints=[SQL("DEFAULT 0")])
    gift_message_id = IntegerField(null=True)
    grand_total = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    hidden_tax_amount = DecimalField(null=True)
    lastname = CharField(null=True)
    middlename = CharField(null=True)
    party_date = DateTimeField(null=True)
    postcode = CharField(null=True)
    prefix = CharField(null=True)
    quote = ForeignKeyField(column_name='quote_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=SalesFlatQuote)
    region = CharField(null=True)
    region_id = IntegerField(null=True)
    same_as_billing = IntegerField(constraints=[SQL("DEFAULT 0")])
    save_in_address_book = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    shipping_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    shipping_description = CharField(null=True)
    shipping_discount_amount = DecimalField(null=True)
    shipping_hidden_tax_amount = DecimalField(null=True)
    shipping_incl_tax = DecimalField(null=True)
    shipping_method = CharField(null=True)
    shipping_tax_amount = DecimalField(null=True)
    street = CharField(null=True)
    subtotal = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    subtotal_incl_tax = DecimalField(null=True)
    subtotal_with_discount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    suffix = CharField(null=True)
    tax_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    telephone = CharField(null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    vat_id = TextField(null=True)
    vat_is_valid = IntegerField(null=True)
    vat_request_date = TextField(null=True)
    vat_request_id = TextField(null=True)
    vat_request_success = IntegerField(null=True)
    weight = DecimalField(constraints=[SQL("DEFAULT 0.0000")])

    class Meta:
        table_name = 'sales_flat_quote_address'

class SalesFlatQuoteItem(BaseModel):
    additional_data = TextField(null=True)
    applied_rule_ids = TextField(null=True)
    base_cost = DecimalField(null=True)
    base_discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    base_hidden_tax_amount = DecimalField(null=True)
    base_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    base_price_incl_tax = DecimalField(null=True)
    base_row_total = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    base_row_total_incl_tax = DecimalField(null=True)
    base_tax_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    base_tax_before_discount = DecimalField(null=True)
    base_weee_tax_applied_amount = DecimalField(null=True)
    base_weee_tax_applied_row_amnt = DecimalField(null=True)
    base_weee_tax_disposition = DecimalField(null=True)
    base_weee_tax_row_disposition = DecimalField(null=True)
    category_cart_add = IntegerField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    custom_price = DecimalField(null=True)
    description = TextField(null=True)
    discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    discount_percent = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    free_shipping = IntegerField(constraints=[SQL("DEFAULT 0")])
    gift_message_id = IntegerField(null=True)
    hidden_tax_amount = DecimalField(null=True)
    is_qty_decimal = IntegerField(null=True)
    is_virtual = IntegerField(null=True)
    item_id = AutoField()
    name = CharField(null=True)
    no_discount = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    original_custom_price = DecimalField(null=True)
    parent_item = ForeignKeyField(column_name='parent_item_id', field='item_id', model='self', null=True)
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    price_incl_tax = DecimalField(null=True)
    product = ForeignKeyField(column_name='product_id', field='entity_id', model=CatalogProductEntity, null=True)
    product_type = CharField(null=True)
    qty = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    quote = ForeignKeyField(column_name='quote_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=SalesFlatQuote)
    redirect_url = CharField(null=True)
    row_total = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    row_total_incl_tax = DecimalField(null=True)
    row_total_with_discount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    row_weight = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    sku = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    tax_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    tax_before_discount = DecimalField(null=True)
    tax_percent = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    weee_tax_applied = TextField(null=True)
    weee_tax_applied_amount = DecimalField(null=True)
    weee_tax_applied_row_amount = DecimalField(null=True)
    weee_tax_disposition = DecimalField(null=True)
    weee_tax_row_disposition = DecimalField(null=True)
    weight = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)

    class Meta:
        table_name = 'sales_flat_quote_item'

class SalesFlatQuoteAddressItem(BaseModel):
    additional_data = TextField(null=True)
    address_item_id = AutoField()
    applied_rule_ids = TextField(null=True)
    base_cost = DecimalField(null=True)
    base_discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    base_hidden_tax_amount = DecimalField(null=True)
    base_price = DecimalField(null=True)
    base_price_incl_tax = DecimalField(null=True)
    base_row_total = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    base_row_total_incl_tax = DecimalField(null=True)
    base_tax_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    description = TextField(null=True)
    discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    discount_percent = DecimalField(null=True)
    free_shipping = IntegerField(null=True)
    gift_message_id = IntegerField(null=True)
    hidden_tax_amount = DecimalField(null=True)
    image = CharField(null=True)
    is_qty_decimal = IntegerField(null=True)
    name = CharField(null=True)
    no_discount = IntegerField(null=True)
    parent_item = ForeignKeyField(column_name='parent_item_id', field='address_item_id', model='self', null=True)
    parent_product_id = IntegerField(null=True)
    price = DecimalField(null=True)
    price_incl_tax = DecimalField(null=True)
    product_id = IntegerField(null=True)
    qty = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    quote_address = ForeignKeyField(column_name='quote_address_id', constraints=[SQL("DEFAULT 0")], field='address_id', model=SalesFlatQuoteAddress)
    quote_item = ForeignKeyField(column_name='quote_item_id', constraints=[SQL("DEFAULT 0")], field='item_id', model=SalesFlatQuoteItem)
    row_total = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    row_total_incl_tax = DecimalField(null=True)
    row_total_with_discount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    row_weight = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    sku = CharField(null=True)
    super_product_id = IntegerField(null=True)
    tax_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    tax_percent = DecimalField(null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    weight = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)

    class Meta:
        table_name = 'sales_flat_quote_address_item'

class SalesFlatQuoteItemOption(BaseModel):
    code = CharField()
    item = ForeignKeyField(column_name='item_id', field='item_id', model=SalesFlatQuoteItem)
    option_id = AutoField()
    product_id = IntegerField()
    value = TextField(null=True)

    class Meta:
        table_name = 'sales_flat_quote_item_option'

class SalesFlatQuotePayment(BaseModel):
    additional_data = TextField(null=True)
    additional_information = TextField(null=True)
    cc_cid_enc = CharField(null=True)
    cc_exp_month = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    cc_exp_year = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    cc_last4 = CharField(null=True)
    cc_number_enc = CharField(null=True)
    cc_owner = CharField(null=True)
    cc_ss_issue = CharField(null=True)
    cc_ss_owner = CharField(null=True)
    cc_ss_start_month = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    cc_ss_start_year = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    cc_type = CharField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    method = CharField(null=True)
    payment_id = AutoField()
    paypal_correlation_id = CharField(null=True)
    paypal_payer_id = CharField(null=True)
    paypal_payer_status = CharField(null=True)
    po_number = CharField(null=True)
    quote = ForeignKeyField(column_name='quote_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=SalesFlatQuote)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])

    class Meta:
        table_name = 'sales_flat_quote_payment'

class SalesFlatQuoteShippingRate(BaseModel):
    address = ForeignKeyField(column_name='address_id', constraints=[SQL("DEFAULT 0")], field='address_id', model=SalesFlatQuoteAddress)
    carrier = CharField(null=True)
    carrier_title = CharField(null=True)
    code = CharField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    error_message = TextField(null=True)
    method = CharField(null=True)
    method_description = TextField(null=True)
    method_title = TextField(null=True)
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    rate_id = AutoField()
    updated_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])

    class Meta:
        table_name = 'sales_flat_quote_shipping_rate'

class SalesFlatShipment(BaseModel):
    billing_address_id = IntegerField(null=True)
    created_at = DateTimeField(index=True, null=True)
    customer_id = IntegerField(null=True)
    email_sent = IntegerField(null=True)
    entity_id = AutoField()
    increment_id = CharField(null=True, unique=True)
    order = ForeignKeyField(column_name='order_id', field='entity_id', model=SalesFlatOrder)
    packages = TextField(null=True)
    shipment_status = IntegerField(null=True)
    shipping_address_id = IntegerField(null=True)
    shipping_label = TextField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    total_qty = DecimalField(index=True, null=True)
    total_weight = DecimalField(null=True)
    updated_at = DateTimeField(index=True, null=True)

    class Meta:
        table_name = 'sales_flat_shipment'

class SalesFlatShipmentComment(BaseModel):
    comment = TextField(null=True)
    created_at = DateTimeField(index=True, null=True)
    entity_id = AutoField()
    is_customer_notified = IntegerField(null=True)
    is_visible_on_front = IntegerField(constraints=[SQL("DEFAULT 0")])
    parent = ForeignKeyField(column_name='parent_id', field='entity_id', model=SalesFlatShipment)

    class Meta:
        table_name = 'sales_flat_shipment_comment'

class SalesFlatShipmentGrid(BaseModel):
    created_at = DateTimeField(index=True, null=True)
    entity = ForeignKeyField(column_name='entity_id', field='entity_id', model=SalesFlatShipment, primary_key=True)
    increment_id = CharField(null=True, unique=True)
    order_created_at = DateTimeField(index=True, null=True)
    order_id = IntegerField(index=True)
    order_increment_id = CharField(index=True, null=True)
    shipment_status = IntegerField(index=True, null=True)
    shipping_name = CharField(index=True, null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    total_qty = DecimalField(index=True, null=True)

    class Meta:
        table_name = 'sales_flat_shipment_grid'

class SalesFlatShipmentItem(BaseModel):
    additional_data = TextField(null=True)
    description = TextField(null=True)
    entity_id = AutoField()
    name = CharField(null=True)
    order_item_id = IntegerField(null=True)
    parent = ForeignKeyField(column_name='parent_id', field='entity_id', model=SalesFlatShipment)
    price = DecimalField(null=True)
    product_id = IntegerField(null=True)
    qty = DecimalField(null=True)
    row_total = DecimalField(null=True)
    sku = CharField(null=True)
    weight = DecimalField(null=True)

    class Meta:
        table_name = 'sales_flat_shipment_item'

class SalesFlatShipmentTrack(BaseModel):
    carrier_code = CharField(null=True)
    created_at = DateTimeField(index=True, null=True)
    description = TextField(null=True)
    entity_id = AutoField()
    order_id = IntegerField(index=True)
    parent = ForeignKeyField(column_name='parent_id', field='entity_id', model=SalesFlatShipment)
    qty = DecimalField(null=True)
    title = CharField(null=True)
    track_number = TextField(null=True)
    updated_at = DateTimeField(null=True)
    weight = DecimalField(null=True)

    class Meta:
        table_name = 'sales_flat_shipment_track'

class SalesInvoicedAggregated(BaseModel):
    invoiced = DecimalField(null=True)
    invoiced_captured = DecimalField(null=True)
    invoiced_not_captured = DecimalField(null=True)
    order_status = CharField(null=True)
    orders_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    orders_invoiced = DecimalField(null=True)
    period = DateField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)

    class Meta:
        table_name = 'sales_invoiced_aggregated'
        indexes = (
            (('period', 'store', 'order_status'), True),
        )

class SalesInvoicedAggregatedOrder(BaseModel):
    invoiced = DecimalField(null=True)
    invoiced_captured = DecimalField(null=True)
    invoiced_not_captured = DecimalField(null=True)
    order_status = CharField(constraints=[SQL("DEFAULT ''")])
    orders_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    orders_invoiced = DecimalField(null=True)
    period = DateField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)

    class Meta:
        table_name = 'sales_invoiced_aggregated_order'
        indexes = (
            (('period', 'store', 'order_status'), True),
        )

class SalesOrderAggregatedCreated(BaseModel):
    order_status = CharField(constraints=[SQL("DEFAULT ''")])
    orders_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    period = DateField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    total_canceled_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_discount_amount_actual = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_income_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_invoiced_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_paid_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_profit_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_qty_invoiced = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_qty_ordered = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_refunded_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_revenue_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_shipping_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_shipping_amount_actual = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_tax_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_tax_amount_actual = DecimalField(constraints=[SQL("DEFAULT 0.0000")])

    class Meta:
        table_name = 'sales_order_aggregated_created'
        indexes = (
            (('period', 'store', 'order_status'), True),
        )

class SalesOrderAggregatedUpdated(BaseModel):
    order_status = CharField()
    orders_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    period = DateField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    total_canceled_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_discount_amount_actual = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_income_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_invoiced_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_paid_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_profit_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_qty_invoiced = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_qty_ordered = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_refunded_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_revenue_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_shipping_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_shipping_amount_actual = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_tax_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_tax_amount_actual = DecimalField(constraints=[SQL("DEFAULT 0.0000")])

    class Meta:
        table_name = 'sales_order_aggregated_updated'
        indexes = (
            (('period', 'store', 'order_status'), True),
        )

class SalesOrderStatus(BaseModel):
    label = CharField()
    status = CharField(primary_key=True)

    class Meta:
        table_name = 'sales_order_status'

class SalesOrderStatusLabel(BaseModel):
    label = CharField()
    status = ForeignKeyField(column_name='status', field='status', model=SalesOrderStatus)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore)

    class Meta:
        table_name = 'sales_order_status_label'
        indexes = (
            (('status', 'store'), True),
        )
        primary_key = CompositeKey('status', 'store')

class SalesOrderStatusState(BaseModel):
    is_default = IntegerField(constraints=[SQL("DEFAULT 0")])
    state = CharField()
    status = ForeignKeyField(column_name='status', field='status', model=SalesOrderStatus)

    class Meta:
        table_name = 'sales_order_status_state'
        indexes = (
            (('status', 'state'), True),
        )
        primary_key = CompositeKey('state', 'status')

class SalesOrderTax(BaseModel):
    amount = DecimalField(null=True)
    base_amount = DecimalField(null=True)
    base_real_amount = DecimalField(null=True)
    code = CharField(null=True)
    hidden = IntegerField(constraints=[SQL("DEFAULT 0")])
    order_id = IntegerField()
    percent = DecimalField(null=True)
    position = IntegerField()
    priority = IntegerField()
    process = IntegerField()
    tax_id = AutoField()
    title = CharField(null=True)

    class Meta:
        table_name = 'sales_order_tax'
        indexes = (
            (('order_id', 'priority', 'position'), False),
        )

class SalesOrderTaxItem(BaseModel):
    item = ForeignKeyField(column_name='item_id', field='item_id', model=SalesFlatOrderItem)
    tax = ForeignKeyField(column_name='tax_id', field='tax_id', model=SalesOrderTax)
    tax_item_id = AutoField()
    tax_percent = DecimalField()

    class Meta:
        table_name = 'sales_order_tax_item'
        indexes = (
            (('tax', 'item'), True),
        )

class SalesPaymentTransaction(BaseModel):
    additional_information = TextField(null=True)
    created_at = DateTimeField(null=True)
    is_closed = IntegerField(constraints=[SQL("DEFAULT 1")])
    order = ForeignKeyField(column_name='order_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=SalesFlatOrder)
    parent = ForeignKeyField(column_name='parent_id', field='transaction_id', model='self', null=True)
    parent_txn_id = CharField(null=True)
    payment = ForeignKeyField(column_name='payment_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=SalesFlatOrderPayment)
    transaction_id = AutoField()
    txn_id = CharField(null=True)
    txn_type = CharField(null=True)

    class Meta:
        table_name = 'sales_payment_transaction'
        indexes = (
            (('order', 'payment', 'txn_id'), True),
        )

class SalesRecurringProfile(BaseModel):
    additional_info = TextField(null=True)
    bill_failed_later = IntegerField(constraints=[SQL("DEFAULT 0")])
    billing_address_info = TextField()
    billing_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    currency_code = CharField()
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity, null=True)
    init_amount = DecimalField(null=True)
    init_may_fail = IntegerField(constraints=[SQL("DEFAULT 0")])
    internal_reference_id = CharField(unique=True)
    method_code = CharField()
    order_info = TextField()
    order_item_info = TextField()
    period_frequency = IntegerField(null=True)
    period_max_cycles = IntegerField(null=True)
    period_unit = CharField()
    profile_id = AutoField()
    profile_vendor_info = TextField(null=True)
    reference_id = CharField(null=True)
    schedule_description = CharField()
    shipping_address_info = TextField(null=True)
    shipping_amount = DecimalField(null=True)
    start_datetime = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    state = CharField()
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    subscriber_name = CharField(null=True)
    suspension_threshold = IntegerField(null=True)
    tax_amount = DecimalField(null=True)
    trial_billing_amount = TextField(null=True)
    trial_period_frequency = IntegerField(null=True)
    trial_period_max_cycles = IntegerField(null=True)
    trial_period_unit = CharField(null=True)
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'sales_recurring_profile'

class SalesRecurringProfileOrder(BaseModel):
    link_id = AutoField()
    order = ForeignKeyField(column_name='order_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=SalesFlatOrder)
    profile = ForeignKeyField(column_name='profile_id', constraints=[SQL("DEFAULT 0")], field='profile_id', model=SalesRecurringProfile)

    class Meta:
        table_name = 'sales_recurring_profile_order'
        indexes = (
            (('profile', 'order'), True),
        )

class SalesRefundedAggregated(BaseModel):
    offline_refunded = DecimalField(null=True)
    online_refunded = DecimalField(null=True)
    order_status = CharField(constraints=[SQL("DEFAULT ''")])
    orders_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    period = DateField(null=True)
    refunded = DecimalField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)

    class Meta:
        table_name = 'sales_refunded_aggregated'
        indexes = (
            (('period', 'store', 'order_status'), True),
        )

class SalesRefundedAggregatedOrder(BaseModel):
    offline_refunded = DecimalField(null=True)
    online_refunded = DecimalField(null=True)
    order_status = CharField(null=True)
    orders_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    period = DateField(null=True)
    refunded = DecimalField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)

    class Meta:
        table_name = 'sales_refunded_aggregated_order'
        indexes = (
            (('period', 'store', 'order_status'), True),
        )

class SalesShippingAggregated(BaseModel):
    order_status = CharField(null=True)
    orders_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    period = DateField(null=True)
    shipping_description = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    total_shipping = DecimalField(null=True)
    total_shipping_actual = DecimalField(null=True)

    class Meta:
        table_name = 'sales_shipping_aggregated'
        indexes = (
            (('period', 'store', 'order_status', 'shipping_description'), True),
        )

class SalesShippingAggregatedOrder(BaseModel):
    order_status = CharField(null=True)
    orders_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    period = DateField(null=True)
    shipping_description = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    total_shipping = DecimalField(null=True)
    total_shipping_actual = DecimalField(null=True)

    class Meta:
        table_name = 'sales_shipping_aggregated_order'
        indexes = (
            (('period', 'store', 'order_status', 'shipping_description'), True),
        )

class Salesrule(BaseModel):
    actions_serialized = TextField(null=True)
    apply_to_shipping = IntegerField(constraints=[SQL("DEFAULT 0")])
    conditions_serialized = TextField(null=True)
    coupon_type = IntegerField(constraints=[SQL("DEFAULT 1")])
    description = TextField(null=True)
    discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    discount_qty = DecimalField(null=True)
    discount_step = IntegerField()
    from_date = DateField(null=True)
    is_active = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_advanced = IntegerField(constraints=[SQL("DEFAULT 1")])
    is_rss = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField(null=True)
    product_ids = TextField(null=True)
    rule_id = AutoField()
    simple_action = CharField(null=True)
    simple_free_shipping = IntegerField(constraints=[SQL("DEFAULT 0")])
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    stop_rules_processing = IntegerField(constraints=[SQL("DEFAULT 1")])
    times_used = IntegerField(constraints=[SQL("DEFAULT 0")])
    to_date = DateField(null=True)
    use_auto_generation = IntegerField(constraints=[SQL("DEFAULT 0")])
    uses_per_coupon = IntegerField(constraints=[SQL("DEFAULT 0")])
    uses_per_customer = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'salesrule'
        indexes = (
            (('is_active', 'sort_order', 'to_date', 'from_date'), False),
        )

class SalesruleCoupon(BaseModel):
    code = CharField(null=True, unique=True)
    coupon_id = AutoField()
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    expiration_date = DateTimeField(null=True)
    is_primary = IntegerField(null=True)
    rule = ForeignKeyField(column_name='rule_id', field='rule_id', model=Salesrule)
    times_used = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    usage_limit = IntegerField(null=True)
    usage_per_customer = IntegerField(null=True)

    class Meta:
        table_name = 'salesrule_coupon'
        indexes = (
            (('rule', 'is_primary'), True),
        )

class SalesruleCouponUsage(BaseModel):
    coupon = ForeignKeyField(column_name='coupon_id', field='coupon_id', model=SalesruleCoupon)
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity)
    times_used = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'salesrule_coupon_usage'
        indexes = (
            (('coupon', 'customer'), True),
        )
        primary_key = CompositeKey('coupon', 'customer')

class SalesruleCustomer(BaseModel):
    customer = ForeignKeyField(column_name='customer_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerEntity)
    rule_customer_id = AutoField()
    rule = ForeignKeyField(column_name='rule_id', constraints=[SQL("DEFAULT 0")], field='rule_id', model=Salesrule)
    times_used = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'salesrule_customer'
        indexes = (
            (('customer', 'rule'), False),
            (('rule', 'customer'), False),
        )

class SalesruleCustomerGroup(BaseModel):
    customer_group = ForeignKeyField(column_name='customer_group_id', field='customer_group_id', model=CustomerGroup)
    rule = ForeignKeyField(column_name='rule_id', field='rule_id', model=Salesrule)

    class Meta:
        table_name = 'salesrule_customer_group'
        indexes = (
            (('rule', 'customer_group'), True),
        )
        primary_key = CompositeKey('customer_group', 'rule')

class SalesruleLabel(BaseModel):
    label = CharField(null=True)
    label_id = AutoField()
    rule = ForeignKeyField(column_name='rule_id', field='rule_id', model=Salesrule)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore)

    class Meta:
        table_name = 'salesrule_label'
        indexes = (
            (('rule', 'store'), True),
        )

class SalesruleProductAttribute(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', field='attribute_id', model=EavAttribute)
    customer_group = ForeignKeyField(column_name='customer_group_id', field='customer_group_id', model=CustomerGroup)
    rule = ForeignKeyField(column_name='rule_id', field='rule_id', model=Salesrule)
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'salesrule_product_attribute'
        indexes = (
            (('rule', 'website', 'customer_group', 'attribute'), True),
        )
        primary_key = CompositeKey('attribute', 'customer_group', 'rule', 'website')

class SalesruleWebsite(BaseModel):
    rule = ForeignKeyField(column_name='rule_id', field='rule_id', model=Salesrule)
    website = ForeignKeyField(column_name='website_id', field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'salesrule_website'
        indexes = (
            (('rule', 'website'), True),
        )
        primary_key = CompositeKey('rule', 'website')

class Secondeyes(BaseModel):
    sku = CharField(primary_key=True)
    upc = CharField()

    class Meta:
        table_name = 'secondEYES'

class SecondEyesCompleted(BaseModel):
    order_number = TextField()
    scanned_by = TextField()
    timestamp = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'second_eyes_completed'

class SecondEyesUpc(BaseModel):
    sku = CharField(unique=True)
    upc = CharField()

    class Meta:
        table_name = 'second_eyes_upc'

class SecondEyesUser(BaseModel):
    password = TextField()
    user = TextField()

    class Meta:
        table_name = 'second_eyes_user'

class SendfriendLog(BaseModel):
    ip = CharField(index=True, null=True)
    log_id = AutoField()
    time = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    website_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'sendfriend_log'

class ShelfApp(BaseModel):
    audited_by = IntegerField(null=True)
    date = DateTimeField(null=True)
    location_id = IntegerField(null=True)
    product_id = IntegerField(null=True)
    status = IntegerField(null=True)

    class Meta:
        table_name = 'shelf_app'

class ShelfAudit(BaseModel):
    audit_end_date = DateField(null=True)
    audit_name = CharField()
    audit_start_date = DateField()
    current = UnknownField(null=True)  # bit
    shelf_audit_id = AutoField()

    class Meta:
        table_name = 'shelf_audit'

class ShelfAuditItems(BaseModel):
    audit_id = IntegerField(null=True)
    audited_by = IntegerField(null=True)
    audited_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    item_id = AutoField()
    location_id = IntegerField(null=True)
    product_id = IntegerField(null=True)
    status = IntegerField(null=True)

    class Meta:
        table_name = 'shelf_audit_items'

class ShippingMatrixrate(BaseModel):
    condition_from_value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    condition_name = CharField(constraints=[SQL("DEFAULT ''")])
    condition_to_value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    cost = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    delivery_type = CharField(constraints=[SQL("DEFAULT ''")])
    dest_city = CharField(constraints=[SQL("DEFAULT ''")])
    dest_country_id = CharField(constraints=[SQL("DEFAULT '0'")])
    dest_region_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    dest_zip = CharField(constraints=[SQL("DEFAULT ''")])
    dest_zip_to = CharField(constraints=[SQL("DEFAULT ''")])
    pk = AutoField()
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    website_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'shipping_matrixrate'
        indexes = (
            (('website_id', 'dest_country_id', 'dest_region_id', 'dest_city', 'dest_zip', 'dest_zip_to', 'condition_name', 'condition_from_value', 'condition_to_value', 'delivery_type'), True),
        )

class ShippingTablerate(BaseModel):
    condition_name = CharField()
    condition_value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    cost = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    dest_country_id = CharField(constraints=[SQL("DEFAULT '0'")])
    dest_region_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    dest_zip = CharField(constraints=[SQL("DEFAULT '*'")])
    pk = AutoField()
    price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    website_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'shipping_tablerate'
        indexes = (
            (('website_id', 'dest_country_id', 'dest_region_id', 'dest_zip', 'condition_name', 'condition_value'), True),
        )

class ShippingZones(BaseModel):
    carrier = CharField(null=True)
    fedex_zone_number = CharField(null=True)
    usps_zone_number = CharField(null=True)
    zipcode = CharField(null=True)
    zone_id = AutoField()
    zone_number = CharField(null=True)

    class Meta:
        table_name = 'shipping_zones'

class ShipworksShippingActivity(BaseModel):
    date = DateTimeField(null=True)
    ship_total = IntegerField(null=True)
    user_id = IntegerField(null=True)

    class Meta:
        table_name = 'shipworks_shipping_activity'

class ShipworksShippingCosts(BaseModel):
    carrier = CharField()
    height = IntegerField(null=True)
    length = IntegerField(null=True)
    order_num = CharField(primary_key=True)
    processed_date = DateField()
    shipped_by = CharField(null=True)
    shipping_cost = DecimalField()
    shipping_fee = DecimalField()
    shipping_service = CharField(null=True)
    shipping_state = CharField(null=True)
    shipping_zipcode = CharField(null=True)
    weight = DecimalField(null=True)
    width = IntegerField(null=True)
    zipcode_short = CharField()
    zone_id = IntegerField(null=True)

    class Meta:
        table_name = 'shipworks_shipping_costs'
        indexes = (
            (('order_num', 'shipping_fee'), True),
        )

class ShipworksShippingCosts2015(BaseModel):
    height = IntegerField(null=True)
    length = IntegerField(null=True)
    order_num = CharField()
    processed_date = DateField()
    shipment_id = AutoField()
    shipped_by = CharField(null=True)
    shipping_cost = DecimalField()
    shipping_fee = DecimalField()
    shipping_service = CharField(null=True)
    shipping_state = CharField(null=True)
    shipping_zipcode = CharField(null=True)
    weight = DecimalField(null=True)
    width = IntegerField(null=True)
    zone_id = IntegerField(null=True)

    class Meta:
        table_name = 'shipworks_shipping_costs_2015'

class Sitemap(BaseModel):
    sitemap_filename = CharField(null=True)
    sitemap_id = AutoField()
    sitemap_path = CharField(null=True)
    sitemap_time = DateTimeField(null=True)
    sitemap_type = CharField(null=True)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)

    class Meta:
        table_name = 'sitemap'

class SmProductsFilter(BaseModel):
    condition_str = TextField()
    filter_str = CharField(null=True)
    search_in_description = IntegerField()

    class Meta:
        table_name = 'sm_products_filter'

class Tag(BaseModel):
    first_customer = ForeignKeyField(column_name='first_customer_id', field='entity_id', model=CustomerEntity, null=True)
    first_store = ForeignKeyField(column_name='first_store_id', field='store_id', model=CoreStore, null=True)
    name = CharField(null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    tag_id = AutoField()

    class Meta:
        table_name = 'tag'

class TagProperties(BaseModel):
    base_popularity = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    tag = ForeignKeyField(column_name='tag_id', constraints=[SQL("DEFAULT 0")], field='tag_id', model=Tag)

    class Meta:
        table_name = 'tag_properties'
        indexes = (
            (('tag', 'store'), True),
        )
        primary_key = CompositeKey('store', 'tag')

class TagRelation(BaseModel):
    active = IntegerField(constraints=[SQL("DEFAULT 1")])
    created_at = DateTimeField(null=True)
    customer = ForeignKeyField(column_name='customer_id', field='entity_id', model=CustomerEntity, null=True)
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 1")], field='store_id', model=CoreStore)
    tag = ForeignKeyField(column_name='tag_id', constraints=[SQL("DEFAULT 0")], field='tag_id', model=Tag)
    tag_relation_id = AutoField()

    class Meta:
        table_name = 'tag_relation'
        indexes = (
            (('tag', 'customer', 'product', 'store'), True),
        )

class TagSummary(BaseModel):
    base_popularity = IntegerField(constraints=[SQL("DEFAULT 0")])
    customers = IntegerField(constraints=[SQL("DEFAULT 0")])
    historical_uses = IntegerField(constraints=[SQL("DEFAULT 0")])
    popularity = IntegerField(constraints=[SQL("DEFAULT 0")])
    products = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    tag = ForeignKeyField(column_name='tag_id', constraints=[SQL("DEFAULT 0")], field='tag_id', model=Tag)
    uses = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tag_summary'
        indexes = (
            (('tag', 'store'), True),
        )
        primary_key = CompositeKey('store', 'tag')

class TaxClass(BaseModel):
    class_id = AutoField()
    class_name = CharField()
    class_type = CharField(constraints=[SQL("DEFAULT 'CUSTOMER'")])

    class Meta:
        table_name = 'tax_class'

class TaxCalculationRate(BaseModel):
    code = CharField(index=True)
    rate = DecimalField()
    tax_calculation_rate_id = AutoField()
    tax_country_id = CharField()
    tax_postcode = CharField(null=True)
    tax_region_id = IntegerField()
    zip_from = IntegerField(null=True)
    zip_is_range = IntegerField(null=True)
    zip_to = IntegerField(null=True)

    class Meta:
        table_name = 'tax_calculation_rate'
        indexes = (
            (('tax_calculation_rate_id', 'tax_country_id', 'tax_region_id', 'zip_is_range', 'tax_postcode'), False),
            (('tax_country_id', 'tax_region_id', 'tax_postcode'), False),
        )

class TaxCalculationRule(BaseModel):
    calculate_subtotal = IntegerField()
    code = CharField(index=True)
    position = IntegerField()
    priority = IntegerField()
    tax_calculation_rule_id = AutoField()

    class Meta:
        table_name = 'tax_calculation_rule'
        indexes = (
            (('priority', 'position', 'tax_calculation_rule_id'), False),
        )

class TaxCalculation(BaseModel):
    customer_tax_class = ForeignKeyField(column_name='customer_tax_class_id', field='class_id', model=TaxClass)
    product_tax_class = ForeignKeyField(backref='tax_class_product_tax_class_set', column_name='product_tax_class_id', field='class_id', model=TaxClass)
    tax_calculation_id = AutoField()
    tax_calculation_rate = ForeignKeyField(column_name='tax_calculation_rate_id', field='tax_calculation_rate_id', model=TaxCalculationRate)
    tax_calculation_rule = ForeignKeyField(column_name='tax_calculation_rule_id', field='tax_calculation_rule_id', model=TaxCalculationRule)

    class Meta:
        table_name = 'tax_calculation'
        indexes = (
            (('tax_calculation_rate', 'customer_tax_class', 'product_tax_class'), False),
        )

class TaxCalculationRateTitle(BaseModel):
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore)
    tax_calculation_rate = ForeignKeyField(column_name='tax_calculation_rate_id', field='tax_calculation_rate_id', model=TaxCalculationRate)
    tax_calculation_rate_title_id = AutoField()
    value = CharField()

    class Meta:
        table_name = 'tax_calculation_rate_title'
        indexes = (
            (('tax_calculation_rate', 'store'), False),
        )

class TaxOrderAggregatedCreated(BaseModel):
    code = CharField()
    order_status = CharField()
    orders_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    percent = FloatField(null=True)
    period = DateField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    tax_base_amount_sum = FloatField(null=True)

    class Meta:
        table_name = 'tax_order_aggregated_created'
        indexes = (
            (('period', 'store', 'code', 'percent', 'order_status'), True),
        )

class TaxOrderAggregatedUpdated(BaseModel):
    code = CharField()
    order_status = CharField()
    orders_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    percent = FloatField(null=True)
    period = DateField(null=True)
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    tax_base_amount_sum = FloatField(null=True)

    class Meta:
        table_name = 'tax_order_aggregated_updated'
        indexes = (
            (('period', 'store', 'code', 'percent', 'order_status'), True),
        )

class TempLive(BaseModel):
    category_id = IntegerField(index=True, null=True)
    product_id = IntegerField(index=True, null=True)
    sku = CharField(null=True)

    class Meta:
        table_name = 'temp_live'

class UniBanner(BaseModel):
    banner_content = TextField()
    banner_id = AutoField()
    banner_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_time = DateTimeField(null=True)
    filename = CharField(constraints=[SQL("DEFAULT ''")])
    link = CharField(constraints=[SQL("DEFAULT ''")])
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    title = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'uni_banner'

class UniBannergroup(BaseModel):
    animation_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    banner_effects = CharField(constraints=[SQL("DEFAULT ''")])
    banner_height = IntegerField(constraints=[SQL("DEFAULT 0")])
    banner_ids = CharField(constraints=[SQL("DEFAULT ''")])
    banner_width = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_time = DateTimeField(null=True)
    group_code = CharField(constraints=[SQL("DEFAULT ''")])
    group_id = AutoField()
    group_name = CharField(constraints=[SQL("DEFAULT ''")])
    link_target = IntegerField(constraints=[SQL("DEFAULT 0")])
    pre_banner_effects = CharField(constraints=[SQL("DEFAULT ''")])
    show_content = IntegerField(constraints=[SQL("DEFAULT 0")])
    show_title = IntegerField(constraints=[SQL("DEFAULT 0")])
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'uni_bannergroup'

class VendorInfo(BaseModel):
    account_id = CharField()
    active = UnknownField(null=True)  # bit
    address = CharField()
    city = CharField()
    contact = CharField()
    contact_email = CharField()
    contact_misc1 = CharField()
    contact_misc2 = CharField()
    contact_phone = CharField()
    email = CharField()
    fax = CharField()
    name = CharField(unique=True)
    phone = CharField()
    state = CharField()
    vendor_id = AutoField()
    website = CharField()
    zip = CharField()

    class Meta:
        table_name = 'vendor_info'

class WarehouseLocations(BaseModel):
    aisle = CharField(null=True)
    aisle_sort = IntegerField(null=True)
    bay = CharField(null=True)
    location_id = AutoField()
    shelf = CharField(null=True)
    shelf_sort = IntegerField(null=True)
    shelf_upc = CharField(null=True)
    x = IntegerField(null=True)
    y = IntegerField(null=True)
    zone_id = IntegerField(null=True)
    zone_sort = IntegerField(null=True)

    class Meta:
        table_name = 'warehouse_locations'

class WarehouseLocationMatrix(BaseModel):
    location = ForeignKeyField(column_name='location_id', field='location_id', model=WarehouseLocations, null=True)
    matrix_id = AutoField()
    product_id = IntegerField(null=True)

    class Meta:
        table_name = 'warehouse_location_matrix'

class WarehouseOverstockCoordinates(BaseModel):
    active = IntegerField(constraints=[SQL("DEFAULT 1")])
    shelf = CharField()
    upc = CharField(index=True)
    x = IntegerField()
    y = IntegerField()

    class Meta:
        table_name = 'warehouse_overstock_coordinates'

class WarehouseProductConverter(BaseModel):
    aisle = CharField(index=True, null=True)
    bay = CharField(index=True, null=True)
    shelf = CharField(index=True)
    x = IntegerField(index=True)
    y = IntegerField(index=True)

    class Meta:
        table_name = 'warehouse_product_converter'

class WarehouseProductCoordinates(BaseModel):
    active = IntegerField(constraints=[SQL("DEFAULT 1")])
    shelf = CharField(index=True)
    upc = CharField(index=True)
    x = IntegerField(index=True)
    y = IntegerField(index=True)

    class Meta:
        table_name = 'warehouse_product_coordinates'

class WarehouseZones(BaseModel):
    zone_id = AutoField()
    zone_name = CharField(null=True)
    zone_sort = IntegerField(null=True)

    class Meta:
        table_name = 'warehouse_zones'

class WeeeDiscount(BaseModel):
    customer_group = ForeignKeyField(column_name='customer_group_id', field='customer_group_id', model=CustomerGroup)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    website = ForeignKeyField(column_name='website_id', constraints=[SQL("DEFAULT 0")], field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'weee_discount'
        primary_key = False

class WeeeTax(BaseModel):
    attribute = ForeignKeyField(column_name='attribute_id', field='attribute_id', model=EavAttribute)
    country = ForeignKeyField(column_name='country', field='country_id', model=DirectoryCountry, null=True)
    entity = ForeignKeyField(column_name='entity_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    entity_type_id = IntegerField()
    state = CharField(constraints=[SQL("DEFAULT '*'")])
    value = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    value_id = AutoField()
    website = ForeignKeyField(column_name='website_id', constraints=[SQL("DEFAULT 0")], field='website_id', model=CoreWebsite)

    class Meta:
        table_name = 'weee_tax'

class Widget(BaseModel):
    parameters = TextField(null=True)
    widget_code = CharField(index=True, null=True)
    widget_id = AutoField()
    widget_type = CharField(null=True)

    class Meta:
        table_name = 'widget'

class WidgetInstance(BaseModel):
    instance_id = AutoField()
    instance_type = CharField(null=True)
    package_theme = CharField(null=True)
    sort_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    store_ids = CharField(constraints=[SQL("DEFAULT '0'")])
    title = CharField(null=True)
    widget_parameters = TextField(null=True)

    class Meta:
        table_name = 'widget_instance'

class WidgetInstancePage(BaseModel):
    block_reference = CharField(null=True)
    entities = TextField(null=True)
    instance = ForeignKeyField(column_name='instance_id', constraints=[SQL("DEFAULT 0")], field='instance_id', model=WidgetInstance)
    layout_handle = CharField(null=True)
    page_for = CharField(null=True)
    page_group = CharField(null=True)
    page_id = AutoField()
    page_template = CharField(null=True)

    class Meta:
        table_name = 'widget_instance_page'

class WidgetInstancePageLayout(BaseModel):
    layout_update = ForeignKeyField(column_name='layout_update_id', constraints=[SQL("DEFAULT 0")], field='layout_update_id', model=CoreLayoutUpdate)
    page = ForeignKeyField(column_name='page_id', constraints=[SQL("DEFAULT 0")], field='page_id', model=WidgetInstancePage)

    class Meta:
        table_name = 'widget_instance_page_layout'
        indexes = (
            (('layout_update', 'page'), True),
        )
        primary_key = False

class Wishlist(BaseModel):
    customer = ForeignKeyField(column_name='customer_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CustomerEntity, unique=True)
    shared = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    sharing_code = CharField(null=True)
    updated_at = DateTimeField(null=True)
    wishlist_id = AutoField()

    class Meta:
        table_name = 'wishlist'

class WishlistItem(BaseModel):
    added_at = DateTimeField(null=True)
    description = TextField(null=True)
    product = ForeignKeyField(column_name='product_id', constraints=[SQL("DEFAULT 0")], field='entity_id', model=CatalogProductEntity)
    qty = DecimalField()
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    wishlist = ForeignKeyField(column_name='wishlist_id', constraints=[SQL("DEFAULT 0")], field='wishlist_id', model=Wishlist)
    wishlist_item_id = AutoField()

    class Meta:
        table_name = 'wishlist_item'

class WishlistItemOption(BaseModel):
    code = CharField()
    option_id = AutoField()
    product_id = IntegerField()
    value = TextField(null=True)
    wishlist_item = ForeignKeyField(column_name='wishlist_item_id', field='wishlist_item_id', model=WishlistItem)

    class Meta:
        table_name = 'wishlist_item_option'

class WordpressAssociationType(BaseModel):
    object = CharField(constraints=[SQL("DEFAULT ''")])
    type_id = AutoField()
    wordpress_object = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'wordpress_association_type'

class WordpressAssociation(BaseModel):
    assoc_id = AutoField()
    object_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    position = IntegerField(constraints=[SQL("DEFAULT 4444")])
    store = ForeignKeyField(column_name='store_id', constraints=[SQL("DEFAULT 0")], field='store_id', model=CoreStore)
    type = ForeignKeyField(column_name='type_id', constraints=[SQL("DEFAULT 0")], field='type_id', model=WordpressAssociationType)
    wordpress_object_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'wordpress_association'

class WpCommentmeta(BaseModel):
    comment_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    meta_id = BigAutoField()
    meta_key = CharField(index=True, null=True)
    meta_value = TextField(null=True)

    class Meta:
        table_name = 'wp_commentmeta'

class WpComments(BaseModel):
    comment_id = BigAutoField(column_name='comment_ID')
    comment_agent = CharField(constraints=[SQL("DEFAULT ''")])
    comment_approved = CharField(constraints=[SQL("DEFAULT '1'")])
    comment_author = TextField()
    comment_author_ip = CharField(column_name='comment_author_IP', constraints=[SQL("DEFAULT ''")])
    comment_author_email = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    comment_author_url = CharField(constraints=[SQL("DEFAULT ''")])
    comment_content = TextField()
    comment_date = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    comment_date_gmt = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")], index=True)
    comment_karma = IntegerField(constraints=[SQL("DEFAULT 0")])
    comment_parent = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    comment_post_id = BigIntegerField(column_name='comment_post_ID', constraints=[SQL("DEFAULT 0")], index=True)
    comment_type = CharField(constraints=[SQL("DEFAULT ''")])
    user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'wp_comments'
        indexes = (
            (('comment_approved', 'comment_date_gmt'), False),
        )

class WpLinks(BaseModel):
    link_description = CharField(constraints=[SQL("DEFAULT ''")])
    link_id = BigAutoField()
    link_image = CharField(constraints=[SQL("DEFAULT ''")])
    link_name = CharField(constraints=[SQL("DEFAULT ''")])
    link_notes = TextField()
    link_owner = BigIntegerField(constraints=[SQL("DEFAULT 1")])
    link_rating = IntegerField(constraints=[SQL("DEFAULT 0")])
    link_rel = CharField(constraints=[SQL("DEFAULT ''")])
    link_rss = CharField(constraints=[SQL("DEFAULT ''")])
    link_target = CharField(constraints=[SQL("DEFAULT ''")])
    link_updated = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    link_url = CharField(constraints=[SQL("DEFAULT ''")])
    link_visible = CharField(constraints=[SQL("DEFAULT 'Y'")], index=True)

    class Meta:
        table_name = 'wp_links'

class WpOptions(BaseModel):
    autoload = CharField(constraints=[SQL("DEFAULT 'yes'")])
    option_id = BigAutoField()
    option_name = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    option_value = TextField()

    class Meta:
        table_name = 'wp_options'

class WpPostmeta(BaseModel):
    meta_id = BigAutoField()
    meta_key = CharField(index=True, null=True)
    meta_value = TextField(null=True)
    post_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'wp_postmeta'

class WpPosts(BaseModel):
    id = BigAutoField(column_name='ID')
    comment_count = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    comment_status = CharField(constraints=[SQL("DEFAULT 'open'")])
    guid = CharField(constraints=[SQL("DEFAULT ''")])
    menu_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    ping_status = CharField(constraints=[SQL("DEFAULT 'open'")])
    pinged = TextField()
    post_author = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    post_content = TextField()
    post_content_filtered = TextField()
    post_date = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    post_date_gmt = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    post_excerpt = TextField()
    post_mime_type = CharField(constraints=[SQL("DEFAULT ''")])
    post_modified = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    post_modified_gmt = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    post_name = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    post_parent = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    post_password = CharField(constraints=[SQL("DEFAULT ''")])
    post_status = CharField(constraints=[SQL("DEFAULT 'publish'")])
    post_title = TextField()
    post_type = CharField(constraints=[SQL("DEFAULT 'post'")])
    to_ping = TextField()

    class Meta:
        table_name = 'wp_posts'
        indexes = (
            (('post_type', 'post_status', 'post_date', 'id'), False),
        )

class WpTermRelationships(BaseModel):
    object_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    term_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    term_taxonomy_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'wp_term_relationships'
        indexes = (
            (('object_id', 'term_taxonomy_id'), True),
        )
        primary_key = CompositeKey('object_id', 'term_taxonomy_id')

class WpTermTaxonomy(BaseModel):
    count = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    description = TextField()
    parent = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    taxonomy = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    term_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    term_taxonomy_id = BigAutoField()

    class Meta:
        table_name = 'wp_term_taxonomy'
        indexes = (
            (('term_id', 'taxonomy'), True),
        )

class WpTermmeta(BaseModel):
    meta_id = BigAutoField()
    meta_key = CharField(index=True, null=True)
    meta_value = TextField(null=True)
    term_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'wp_termmeta'

class WpTerms(BaseModel):
    name = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    slug = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    term_group = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    term_id = BigAutoField()

    class Meta:
        table_name = 'wp_terms'

class WpUsermeta(BaseModel):
    meta_key = CharField(index=True, null=True)
    meta_value = TextField(null=True)
    umeta_id = BigAutoField()
    user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'wp_usermeta'

class WpUsers(BaseModel):
    id = BigAutoField(column_name='ID')
    display_name = CharField(constraints=[SQL("DEFAULT ''")])
    user_activation_key = CharField(constraints=[SQL("DEFAULT ''")])
    user_email = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    user_login = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    user_nicename = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    user_pass = CharField(constraints=[SQL("DEFAULT ''")])
    user_registered = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    user_status = IntegerField(constraints=[SQL("DEFAULT 0")])
    user_url = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'wp_users'

class XmlconnectApplication(BaseModel):
    active_from = DateField(null=True)
    active_to = DateField(null=True)
    application_id = AutoField()
    browsing_mode = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    code = CharField(unique=True)
    name = CharField()
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = ForeignKeyField(column_name='store_id', field='store_id', model=CoreStore, null=True)
    type = CharField()
    updated_at = DateTimeField(null=True)

    class Meta:
        table_name = 'xmlconnect_application'

class XmlconnectConfigData(BaseModel):
    application = ForeignKeyField(column_name='application_id', field='application_id', model=XmlconnectApplication)
    category = CharField(constraints=[SQL("DEFAULT 'default'")])
    path = CharField()
    value = TextField()

    class Meta:
        table_name = 'xmlconnect_config_data'
        indexes = (
            (('application', 'category', 'path'), True),
        )
        primary_key = False

class XmlconnectHistory(BaseModel):
    activation_key = CharField()
    application = ForeignKeyField(column_name='application_id', field='application_id', model=XmlconnectApplication)
    code = CharField()
    created_at = DateTimeField(null=True)
    history_id = AutoField()
    name = CharField()
    params = TextField(null=True)
    store_id = IntegerField(null=True)
    title = CharField()

    class Meta:
        table_name = 'xmlconnect_history'

class XmlconnectImages(BaseModel):
    application = ForeignKeyField(column_name='application_id', field='application_id', model=XmlconnectApplication)
    image_file = CharField()
    image_id = AutoField()
    image_type = CharField()
    order = IntegerField()

    class Meta:
        table_name = 'xmlconnect_images'

class XmlconnectNotificationTemplate(BaseModel):
    application = ForeignKeyField(column_name='application_id', field='application_id', model=XmlconnectApplication)
    content = TextField()
    created_at = DateTimeField(null=True)
    message_title = CharField()
    modified_at = DateTimeField(null=True)
    name = CharField()
    push_title = CharField()
    template_id = AutoField()

    class Meta:
        table_name = 'xmlconnect_notification_template'

class XmlconnectQueue(BaseModel):
    content = TextField(null=True)
    create_time = DateTimeField(null=True)
    exec_time = DateTimeField(null=True)
    message_title = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    push_title = CharField()
    queue_id = AutoField()
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    template = ForeignKeyField(column_name='template_id', field='template_id', model=XmlconnectNotificationTemplate)
    type = CharField()

    class Meta:
        table_name = 'xmlconnect_queue'

class XtcoreConfigData(BaseModel):
    config_id = AutoField()
    path = CharField(constraints=[SQL("DEFAULT 'general'")], unique=True)
    value = TextField()

    class Meta:
        table_name = 'xtcore_config_data'

class XtentoProductexportDestination(BaseModel):
    custom_class = CharField()
    custom_function = CharField()
    destination_id = AutoField()
    do_retry = IntegerField(constraints=[SQL("DEFAULT 1")])
    email_attach_files = IntegerField(constraints=[SQL("DEFAULT 1")])
    email_body = TextField()
    email_recipient = CharField()
    email_sender = CharField()
    email_subject = CharField()
    ftp_pasv = IntegerField(constraints=[SQL("DEFAULT 1")])
    ftp_type = CharField()
    hostname = CharField()
    last_modification = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    last_result = IntegerField()
    last_result_message = TextField()
    name = CharField()
    password = CharField()
    path = CharField()
    port = IntegerField(null=True)
    timeout = IntegerField(constraints=[SQL("DEFAULT 15")])
    type = CharField()
    username = CharField()

    class Meta:
        table_name = 'xtento_productexport_destination'

class XtentoProductexportLog(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    destination_ids = TextField()
    export_event = CharField()
    export_type = IntegerField()
    files = TextField()
    log_id = AutoField()
    profile_id = IntegerField()
    records_exported = IntegerField()
    result = IntegerField()
    result_message = TextField()

    class Meta:
        table_name = 'xtento_productexport_log'
        indexes = (
            (('profile_id', 'created_at'), False),
        )

class XtentoProductexportProfile(BaseModel):
    attributes_to_select = TextField()
    conditions_serialized = TextField()
    cronjob_custom_frequency = CharField()
    cronjob_enabled = IntegerField(constraints=[SQL("DEFAULT 0")])
    cronjob_frequency = CharField()
    customer_group_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    destination_ids = CharField()
    enabled = IntegerField()
    encoding = CharField()
    entity = CharField()
    event_observers = CharField()
    export_filter_datefrom = DateField(null=True)
    export_filter_dateto = DateField(null=True)
    export_filter_instock_only = IntegerField(constraints=[SQL("DEFAULT 0")])
    export_filter_last_x_days = IntegerField(null=True)
    export_filter_new_only = IntegerField()
    export_filter_product_status = CharField(constraints=[SQL("DEFAULT ''")])
    export_filter_product_type = CharField()
    export_filter_product_visibility = CharField(constraints=[SQL("DEFAULT ''")])
    export_filter_status = CharField()
    export_filter_updated_last_x_minutes = IntegerField(null=True)
    export_one_file_per_object = IntegerField(constraints=[SQL("DEFAULT 0")])
    export_replace_nl_br = IntegerField(constraints=[SQL("DEFAULT 1")])
    export_strip_tags = IntegerField(constraints=[SQL("DEFAULT 0")])
    export_url_remove_store = IntegerField(constraints=[SQL("DEFAULT 0")])
    filename = CharField()
    last_execution = DateTimeField(null=True)
    last_modification = DateTimeField(null=True)
    manual_export_enabled = IntegerField(constraints=[SQL("DEFAULT 1")])
    name = CharField(constraints=[SQL("DEFAULT ''")])
    output_type = CharField(constraints=[SQL("DEFAULT 'xsl'")])
    profile_id = AutoField()
    save_files_local_copy = IntegerField(constraints=[SQL("DEFAULT 1")])
    save_files_manual_export = IntegerField(constraints=[SQL("DEFAULT 1")])
    start_download_manual_export = IntegerField(constraints=[SQL("DEFAULT 1")])
    store_ids = TextField()
    test_id = CharField()
    xsl_template = TextField()

    class Meta:
        table_name = 'xtento_productexport_profile'

class XtentoProductexportProfileHistory(BaseModel):
    entity = CharField()
    entity_id = IntegerField(index=True)
    exported_at = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")])
    history_id = AutoField()
    log_id = IntegerField()
    profile_id = IntegerField(index=True)

    class Meta:
        table_name = 'xtento_productexport_profile_history'
        indexes = (
            (('entity', 'entity_id'), False),
        )

