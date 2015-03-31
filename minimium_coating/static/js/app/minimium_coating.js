/**
 * Created by diego on 3/23/15.
 */

$(document).ready(function(){
    'use strict';

    $('#form_minimium_coating').submit(function(evt){
        evt.preventDefault();
        var url = $(this).data('url');
        var data = $(this).serialize();
        $.ajax({
            url: url,
            type: 'POST',
            async: true,
            data: data,
            success: process_response,
            error: error_message
        });
    });

    function process_response(response){
        var html = '<ol>'
        $.each(response.data, function( index, value ) {
            html += '<li>' + value + '</li>';
        });
        html += '</ol>'
        $('.results').html(html);
    }

    function error_message(msm){
        console.log('error: ');
    }
})