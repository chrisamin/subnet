/*
    index.js

    This is a Django template containing the JavaScript used on the index page.
    It has available it it the jQuery API and a Django form object.
 */

var exclusive_inputs = {{ form.exclusive_inputs_json }}; 

function modify_other_inputs(el, modify_function) {
    /*
    Given a DOM or jQuery element `el`, apply function `modify_function`
    to all other elements in `el`'s group within exclusive_inputs.
     */
    var el = $(el);
    var this_name = el.attr("name");
    for (inputs_i in exclusive_inputs) {
        var inputs = exclusive_inputs[inputs_i];
        if ($.inArray(this_name, inputs) != -1) {
            for (input_i in inputs) {
                var input = inputs[input_i];
                if (this_name != input) {
                    var other_el = $("input[name=" + input + "]");
                    modify_function(other_el);
                }
            }
        }
    }
}

function update_form(form_el) {
    /*
    Given a form element, update with a new set of network information.
     */
    var url = "{{ request.path }}json/";
    var input = $(form_el).serialize();;
    var json = $.getJSON(url, input, function(data, textStatus, jqXHR) {
        for (key in data) {
            $("input[name=" + key + "]").val(data[key]);
        }
    });
}

$(function() {
    // Make any mutually exclusive fields readonly while the user is
    // focusing on a particular input.
    $("input").focus(function() {
        modify_other_inputs(this, function(other_el) {
            other_el.attr("readonly", "readonly");
            other_el.attr("temporarilyReadonly", "true");
        });
    });

    // Remove temporary readonly attributes when the user is done editing
    // an exclusive field.
    $("input").focusout(function() {
        $("input[temporarilyReadonly]").removeAttr("readonly");
    });

    // Clear mutually exclusive fields when the user changes a particular
    // input.
    $("input").change(function() {
        if ($(this).val()) {
            modify_other_inputs(this, function(other_el) {
                other_el.val("");
            });
        }
        update_form($(this).closest("form"));
    });

    $("form").submit(function() {
        update_form(this);
        return false;
    });

    $("input[type=submit]").hide();
});
