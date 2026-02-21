// ==UserScript==
// @name         一个简单的刷课脚本（最小修改版）
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  修复视频未找到和SPA不生效的问题（最小修改）
// @author       Xuanyansx
// @match        https://hunan.bjewaytech.com/*
// @icon         https://hunan.bjewaytech.com/static/upload/config/8d4e951f-2406-48e1-93b3-78a055d7deeb.ico
// @grant        unsafeWindow
// @run-at       document-end
// ==/UserScript==

(function () {
    'use strict';

    window.addEventListener('load', () => {
        let bool = false;
        let checkInterval;


        function main(b = false) {

            if (b) {
                autoHandleTasks();
            }

            let btn = document.createElement("button");
            btn.innerHTML = "刷课";
            btn.className = "shuakeBtn";
            console.error("七七可爱捏");
            console.log('页面所有资源已加载完毕');

            btn.onclick = function () {
                // 启动自动任务监听
                autoHandleTasks();
                console.log("已开启自动任务");
                btn.disabled = true;
                bool = true;
            };

            let headerBox = document.querySelector('.header_box');
            let btn1 = document.querySelector('.shuakeBtn');
            if (headerBox && !btn1) {
                headerBox.append(btn);
            }
        }

        function autoHandleTasks() {
            const check = () => {
                const video = document.querySelector("video");
                if (video && video.paused) {
                    video.play();
                }

                const dialog = document.querySelector('div.el-dialog[aria-label="答题卡"]');
                if (dialog) {
                    const firstOption = dialog.querySelector('.el-radio');
                    if (firstOption) {
                        firstOption.click();
                        setTimeout(() => {
                            const submitBtn = dialog.querySelector('.el-button span');
                            if (submitBtn) {
                                submitBtn.click();

                                clearInterval(checkInterval);
                            }
                        }, 500);
                    }
                }
            };

            check();

            checkInterval = setInterval(check, 1000);
        }

        main();

        // 原有页面切换检测
        const observer = new MutationObserver(function (mutations) {
            for (let mutation of mutations) {
                for (let node of mutation.addedNodes) {
                    if (node.querySelector &&
                        (node.querySelector('video') || node.querySelector('.header_box'))) {
                        main(bool);
                        break;
                    }
                }
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
})();