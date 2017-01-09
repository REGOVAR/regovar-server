



var sample_selection_table_header    = "<table id=\"browser_samples_table\" class=\"table table-striped table-bordered\" cellspacing=\"0\" width=\"100%\" style=\"margin:0;\"><thead><tr><th style=\"width:30px;\"></th><th>Sample</th>{0}</tr></thead><tbody></tbody></table>";
var sample_selection_table_row       = "<tr id=\"browser_samples_table_{0}\"><td><button class=\"fa delete\" onclick=\"javascript:ui.remove_sample(this);\"> </button></td><td><input type=\"text\" placeholder=\"{1}\" value=\"{2}\" onchange=\"javascript:ui.update_sample_nickname({0}, this);\"/></td>{3}</tr>";
var sample_selection_table_attribute = "<{0}><input type=\"text\" placeholder=\"{1}\" value=\"{2}\" onchange=\"javascript:ui.validate_attribute(this);\"/></{0}>";



var analysis_title_template = "<i class=\"fa fa-folder-o\" style=\"width:20px; text-align:center; margin-right:20px;\" aria-hidden=\"true\"></i>{0}";






// filter_condition_template.format('check', 'DP > 400');
var filter_condition_template = "<li class=\"condition {0}\">\
    <button onclick=\"javascript:filter_toggle_condition(this);\">\
        <i class=\"fa\" aria-hidden=\"true\">&nbsp;</i>\
        <span>{1}</span>\
    </button>\
    <button class=\"fa delete\" onclick=\"javascript:ui.remove_afilter_condition(this);\">&nbsp;</button>\
    <button class=\"fa edit\" onclick=\"javascript:ui.edit_afilter_condition(this);\">&nbsp;</button>\
    <input type=\"hidden\" value='{2}'' />\
</li>";


var filter_set_template = "<li class=\"condition {0}\">\
    <button onclick=\"javascript:filter_toggle_condition(this);\">\
        <i class=\"fa\" aria-hidden=\"true\">&nbsp;</i>\
        <span>{1} <b class=\"fa {2}\" aria-hidden=\"true\"></b> {3}</span>\
    </button>\
    <button class=\"fa delete\" onclick=\"javascript:ui.remove_afilter_condition(this);\">&nbsp;</button>\
    <button class=\"fa edit\" onclick=\"javascript:ui.edit_afilter_condition(this);\">&nbsp;</button>\
    <input type=\"hidden\" value='{4}'' />\
</li>";


// filter_group_template.format('check', 'or', '', 'checked', '', '...');
var filter_group_template = "<li class=\"condition {0}\">\
    <button onclick=\"javascript:filter_toggle_condition(this);\">\
        <i class=\"fa\" aria-hidden=\"true\">&nbsp;</i> \
    </button>\
    <button class=\"fa delete\" onclick=\"javascript:ui.remove_afilter_condition(this);\">&nbsp;</button>\
    <button class=\"fa toggle minus\" onclick=\"javascript:ui.toggle_afilter_condition(this);\">&nbsp;</button>\
    <select name=\"select\" class=\"{1}\" onmouseup=\"javascript:filter_switch_operator(this);\">\
        <option value=\"AND\" {2}>AND</option> \
        <option value=\"OR\" {3}>OR</option>\
        <option value=\"XOR\" {4}>XOR</option>\
    </select>\
    <ul class=\"{1}\">\
        {5}\
        <li class=\"addcondition\">\
            <button href=\"#modal_filter_add_condition\" data-toggle=\"modal\" onclick=\"add_filter_ui_parent_elmt=$(this).parent();\">\
                <b class=\"fa fa-plus\" aria-hidden=\"true\">&nbsp;</b>\
                <span>Add new condition</span>\
            </button>\
        </li>\
    </ul>\
</li>";

var filter_save_filter_empty = "<li class=\"empty_selection\">No filter saved</li>";
var filter_save_filter_row = "<li><a href=\"javascript:ui.reset_filter({0});\"><i class=\"fa fa-cube\" aria-hidden=\"true\" style=\"width:20px; text-align:center;\">&nbsp;</i>{1}</a></li>";
