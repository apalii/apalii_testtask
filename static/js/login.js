/**
 * Created by apalii on 25.01.16.
 */

function input(el) {
    var container = document.getElementById("number");
    var len = container.value.length;
    if (len <= 18) {
        container.value += el.value;
        origLen = container.value.replace(/-/g, '').length
        if (origLen % 4 == 0 && Math.floor(origLen / 4) <= 3) {
            container.value += '-'
        }
    }
}

function input_pin(el) {
    var container = document.getElementById("pin");
    var len = container.value.length;
    if (len < 4) {
        container.value += el.value;
    }
}

$(document).ready(function() {
    $('#1').on('submit', function() {
        return $('#number').val().toString().length === 19;
    });
});

(function() {

    var API = (function() {

        var URLS = {
            check: '/check/',
            auth: '/auth/'
        };

        var sendRequest = function(action, request, callback) {
            return $.ajax({
                url: URLS[action],
                method: action === 'check' ? 'GET' : 'POST',
                type: 'json',
                data: request,
                success: callback
            });
        };

        var check = function(request, callback) {
            sendRequest('check', request, callback);
        };

        var auth = function(request, callback) {
            sendRequest('auth', request, callback).
                fail(function (er){
                    var response = JSON.parse(er.responseText);
                    if (response.tries > 0) {
                        alert(response.message);
                        console.log("Tries :", response.tries);
                    }
                    else {
                        window.location.href = '/blocked/';
                    }
                });
        };

        return {
            check: check,
            auth: auth
        };
    })();

    var init = function() {
        var checkForm = $('#1'),
            authForm = $('#2');

        var number = null;

        var continueCheck = function(response) {
            if (response && response.valid && response.is_active) {
                // hide first form and show the second
                checkForm.hide();
                authForm.show();
                number = response.number_requested;
            }
            else {
                alert("Card is invalid. Please contact support department.");
            }
        };

        var continueAuth = function(response) {
            console.log('auth:', response, response.success);
            if (response && response.success) {
                window.location.href = '/operations/';
            }
        };

        checkForm.find('.btn').last().click(function() {
            var request = checkForm.serialize();
            API.check(request, continueCheck);
            return false;
        });

        authForm.find('.btn').last().click(function() {
            var request = authForm.serialize();
            request += '&number=' + number;
            API.auth(request, continueAuth);
            return false;
        });
    };

    $(document).ready(init);
})();