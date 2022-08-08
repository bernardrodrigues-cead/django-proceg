$(function(){
    $('.maskedCpf').mask('000.000.000-00', {reverse: true});
    $('.maskedCep').mask('00000-000');
    $('.maskedCnpj').mask('00.000.000/0000-00', {reverse: true});
    $('.maskedPhoneBR').mask('(00) 000000000');
    $('.maskedDate').mask('00/00/0000');
    $('.maskedTime').mask('00:00');
    $('.maskedEdital').mask('000');
    $('.maskedAno').mask('0000');
    $('#id_ddd1').mask('(00)');
    $('#id_ddd2').mask('(00)');
});