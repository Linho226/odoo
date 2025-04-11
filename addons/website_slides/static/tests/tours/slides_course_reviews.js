/** @odoo-module **/

import { registry } from "@web/core/registry";

/**
 * This tour test that a log note isn't considered
 * as a course review. And also that a member can
 * add only one review and react to them.
 */
registry.category("web_tour.tours").add("course_reviews", {
    url: "/slides",
    steps: () => [
        {
            trigger: "a:contains(Basics of Gardening - Test)",
            run: "click",
        },
        {
            trigger: "a[id=review-tab]",
            run: "click",
        },
        {
            trigger:
                "#chatterRoot:shadow .o-mail-Chatter-content:not(:has(.o-mail-Message-content))",
        },
        {
            // If it fails here, it means the log note is considered as a review
            trigger: "span:contains(Add Review)",
            run: "click",
        },
        {
            trigger: ".modal.modal_shown.show div.o_portal_chatter_composer_body textarea",
            run: "edit Great course!",
        },
        {
            trigger: ".modal.modal_shown.show button.o_portal_chatter_composer_btn",
            run: "click",
        },
        {
            trigger: "a[id=review-tab]",
            run: "click",
        },
        {
            // If it fails here, it means the system is allowing you to add another review.
            trigger: "span:contains(Edit Review)",
            run: "click",
        },
        {
            trigger: "div.o_portal_chatter_composer_body textarea:value(Great course!)",
            run: "edit Mid course!",
        },
        {
            trigger: ".modal.modal_shown.show button.o_portal_chatter_composer_btn",
            run: "click",
        },
        {
            content: "Reload page (fetch message)",
            trigger: "#chatterRoot:shadow .o-mail-Chatter",
            run() {
                location.reload();
            },
        },
        {
            trigger: "a[id=review-tab]",
            run: "click",
        },
        {
            trigger: "#chatterRoot:shadow .o-mail-Message-textContent:contains(Mid course!)",
            run: "hover && click",
        },
        {
            trigger: "#chatterRoot:shadow .o-mail-Message [title='Add a Reaction']",
            run: "click",
        },
        {
            trigger: "#chatterRoot:shadow .o-Emoji[data-codepoints='😃']",
            run: "click",
        },
        {
            trigger: "#chatterRoot:shadow .o-mail-Message .o-mail-MessageReactions-add:not(:visible)",
        },
        {
            trigger: "#chatterRoot:shadow .o-mail-Message .o-mail-MessageReaction",
            run: "click",
        },
    ],
});
