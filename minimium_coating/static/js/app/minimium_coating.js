/**
 * Created by diego on 3/23/15.
 */

$(document).ready(function(){
    'use strict';

    var tittle_results = ''; // Variable to save the title results click

    $('#form_minimium_coating').submit(function(evt){
        evt.preventDefault();
        var url = $(this).data('url');
        var data = $(this).serialize();
        tittle_results = 'Recubrimiento minimo';
        $.ajax({
            url: url,
            type: 'POST',
            async: true,
            data: data,
            success: process_response,
            error: error_message
        });
    });

    $('#form_candidate_key').submit(function(evt){
        evt.preventDefault();
        var url = $(this).data('url');
        var data = $(this).serialize();
        tittle_results = 'Llaves candidatas';
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
        $('#title_results').html(tittle_results);
        var html = '<ol>'
        $.each(response.data, function( index, value ) {
            html += '<li>' + value + '</li>';
        });
        html += '</ol>'
        $('.results').html(html);

        var html = '<ul>'
        $.each(response.steps, function( index, value ) {
            html += '<li>' + value + '</li>';
        });
        html += '</ul>'
        $('.details_results').html(html);
    }

    function error_message(msm){
        console.log('error: ');
    }
})