$(function () {
    // 点击一级菜单切换显示二级菜单
    $('.multi-menu .item .title').click(function () {
        $(this).next().toggle(100);
    })
})