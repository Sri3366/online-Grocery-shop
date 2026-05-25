(function ($) {
    $.fn.picZoomer = function (options) {
        var opts = $.extend({}, $.fn.picZoomer.defaults, options),
            $this = this,
            $picBD = $('<div class="picZoomer-pic-wp"></div>')
                .css({ width: opts.picWidth + "px", height: opts.picHeight + "px" })
                .appendTo($this),
            $pic = $this.children("img").addClass("picZoomer-pic").appendTo($picBD),
            $cursor = $('<div class="picZoomer-cursor"><i class="f-is picZoomCursor-ico"></i></div>').appendTo($picBD),
            cursorSizeHalf = { w: $cursor.width() / 2, h: $cursor.height() / 2 },
            $zoomWP = $('<div class="picZoomer-zoom-wp"><img src="" alt="" class="picZoomer-zoom-pic"></div>').appendTo($this),
            $zoomPic = $zoomWP.find(".picZoomer-zoom-pic"),
            picBDOffset = { x: $picBD.offset().left, y: $picBD.offset().top };

        opts.zoomWidth = opts.zoomWidth || opts.picWidth;
        opts.zoomHeight = opts.zoomHeight || opts.picHeight;
        var zoomWPSizeHalf = { w: opts.zoomWidth / 2, h: opts.zoomHeight / 2 };

        $zoomWP.css({ width: opts.zoomWidth + "px", height: opts.zoomHeight + "px" });
        $zoomWP.css(opts.zoomerPosition || { top: 0, left: opts.picWidth + 30 + "px" });
        $zoomPic.css({ width: opts.picWidth * opts.scale + "px", height: opts.picHeight * opts.scale + "px" });

        $picBD.on("mouseenter", function () {
            $cursor.show();
            $zoomWP.show();
            $zoomPic.attr("src", $pic.attr("src"));
        }).on("mouseleave", function () {
            $cursor.hide();
            $zoomWP.hide();
        }).on("mousemove", function (event) {
            var x = event.pageX - $picBD.offset().left,
                y = event.pageY - $picBD.offset().top;

            $cursor.css({ left: x - cursorSizeHalf.w + "px", top: y - cursorSizeHalf.h + "px" });
            $zoomPic.css({ left: -(x * opts.scale - zoomWPSizeHalf.w) + "px", top: -(y * opts.scale - zoomWPSizeHalf.h) + "px" });
        });
        return $this;
    };
    $.fn.picZoomer.defaults = {
        picWidth: 380,
        picHeight: 380,
        scale: 2.2,
        zoomerPosition: { top: "0", left: "410px" },
        zoomWidth: 400,
        zoomHeight: 380
    };
})(jQuery);

$(document).ready(function () {
    // 🟢 OPTIMIZED: Initialize zoom layout with responsive-safe options
    if($(".picZoomer").length) {
        $(".picZoomer").picZoomer({
            picWidth: 400,        // Matches image container box nicely
            picHeight: 400,       
            scale: 2.5,           // Clean, sharp zoom details ratio
            zoomWidth: 450,       // Large preview box width
            zoomHeight: 400,      
            zoomerPosition: { top: "0", left: "420px" } // Pushes zoom box safely into the blank space to the right
        });
    }

    // Recommendation Section Owl Carousel Engine instantiation settings
    var owl = $("#recent_post");
    if(owl.length) {
        owl.owlCarousel({
            margin: 20,
            dots: false,
            nav: false,
            autoplay: true,
            autoplayHoverPause: true,
            responsive: {
                0: { items: 1 },
                576: { items: 2 },
                768: { items: 3 },
                992: { items: 4 }
            }
        });
    }

    // Premium Quantity Incrementer/Decrementer Logic
    $(".increase_").click(function () {
        var inputField = $(this).siblings("input#number");
        var currentVal = parseInt(inputField.val(), 10);
        currentVal = isNaN(currentVal) ? 1 : currentVal;
        currentVal++;
        inputField.val(currentVal);
        $("#hidden-cart-qty").val(currentVal); // Keeps hidden form input fields in sync
    });

    $(".decrease_").click(function () {
        var inputField = $(this).siblings("input#number");
        var currentVal = parseInt(inputField.val(), 10);
        currentVal = isNaN(currentVal) ? 1 : currentVal;
        if (currentVal > 1) {
            currentVal--;
            inputField.val(currentVal);
            $("#hidden-cart-qty").val(currentVal);
        }
    });
});