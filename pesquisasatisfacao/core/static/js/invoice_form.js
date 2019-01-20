$(document).ready(function () {

  $('form table tbody tr').formset({
    deleteText: '<i class="material-icons">&#xE872;</i>',
    deleteCssClass: 'btn-floating btn-large waves-effect waves-light red',
    addText: '<i class="material-icons">add</i> Add novo item',
    addCssClass: 'btn-floating btn-large waves-effect waves-light blue',
    prefix: 'items'
  });

});

//BOOTSTRAP
//Referente a figura do botão delete item
//Referente ao css do botão delete item
//Referente a figura e descrição do botão add item
//Referente a tipo e cor do botão add item
//Respectivamente, falta o prefix que não descobri.