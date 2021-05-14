# Nekomoekissaten-MIR-Subs
Subtitles made by MIR in Nekomoe kissaten Fansub.  
License: CC BY-NC-ND 4.0，具体见 [Nekomoekissaten-Subs #注意事项](https://github.com/Nekomoekissaten-SUB/Nekomoekissaten-Subs#-%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A1%B9)

## 注意

本字幕库内自 2021-04-01 起的 Fansub ASS 字幕均基于 [libass](https://github.com/libass/libass) 0.15.0 及之后最新版本制作，之前基于 xy-VSFilter 制作的旧字幕正在逐步检查以在 libass 0.15.0+ 下正常显示。同时会尽力保证 [xy-VSFilter](https://github.com/HomeOfVapourSynthEvolution/xy-VSFilter) 和 [xySubFilter](https://github.com/pinterf/xy-VSFilter) 最新版本的渲染效果，详见[不一致渲染的情况](#不一致渲染的情况)，如有问题欢迎回报 / open issue。

### 可以正确渲染的推荐环境配置

以下均优先考虑最新 release

#### ASS 制作

一切以 libass 0.15.0+ 作为字幕渲染核心的字幕制作软件，包括且不限于[Aegisub wangqr fork](https://github.com/wangqr/Aegisub) v3.3.2+、[Aegisub TypesettingTools ver.](https://github.com/TypesettingTools/Aegisub)。

#### ASS 压制

Avisynth:
 - [AssRender](https://github.com/pinterf/assrender)

Vapoursynth:
 - [AssRender-Vapoursynth](https://github.com/Masaiki/assrender)
 - [VSFilterMod](https://github.com/sorayuki/VSFilterMod) r5.2.4+（忽略[不一致渲染的情况](#不一致渲染的情况)中的第三点时）
 - 使用 libass 0.15.0+ 作为依赖编译的 Subtext（未做测试）

#### ASS 播放

- [mpv](https://mpv.io/installation/) 配置 `sub-ass-vsfilter-blur-compat=no`
- [VLC](https://www.videolan.org/)（未做测试）

#### 不一致渲染的情况

下列主要为测试的一些 libass 与 xySubFilter 等主流 VSFilter 不一致渲染的情况，播放端如何避免或解决问题，以及我的处理

1. `\frx` `\fry` 在 ASS 分辨率（`PlayResX`、`PlayResY`）与播放视频分辨率不同时的渲染效果  
    以 ASS 分辨率与视频分辨率相同时的渲染效果为正确，[参考对比图](https://slow.pics/c/KDV5mZDv)
    - 错误：xy-VSFilter
    - 正确：
        - xySubFilter 设置 `More - Renderer layout options - Customize`
        - MPC-BE / MPC-HC 内置的 VSFilter
        - VSFilterMod r5.2.4+
        - mpv 配置 `sub-ass-vsfilter-blur-compat=no`
    - 处理：以正确效果为准

2. `\p` 大于 1 时的缩放效果
    - 错误：MPC-BE 内置的 VSFilter
    - 正确：xy-VSFilter、xySubFilter、VSFilterMod、mpv
    - 处理：以正确效果为准

3. `bord` `shad` `blur` 的渲染效果  
    - 错误：xySubFilter 等 VSFilter
    - 正确：mpv 配置 `sub-ass-vsfilter-blur-compat=no`
    - 处理：影响较小，一般忽略此类标签的效果不同，特殊情况另做分析

4. 部分字体的竖排效果，如 `\fn@Source Han Sans`  
    - 错误：所有 VSFilter 系滤镜，应该是 GDI 的问题？目前无法解决
    - 正确：所有基于 libass 的字幕滤镜
    - 处理：由于这个问题在 Windows 下难以解决，所以不使用此类字体标签

5. `fay` 的渲染效果
    - libass 在 0.15.1 中使其与 xy-VSFilter 系保持一致
    - 处理：以 xy-VSFilter / libass 0.15.1+ 效果为准

6. 缺失字体或字符时的字体 Fallback
    - 以简体中文 Windows 10 为例，VSFilter Fallback 到中易宋体，libass Fallback 到微软雅黑（？）
    - 处理：制作时应避免出现字符尤其是特殊字符的缺失，同时希望观看者无论何时都推荐安装或挂载 ASS 中使用的所有相应版本的字体

7. ASS 中颜色的色彩空间
    - 最初的 VSFilter 和 r5.2.3 之前的 VSFilterMod 无论何时都只会按照 BT.601 做 YCbCr 和 RGB 之间的颜色转换，xy-VSFilter 在 ASS 头部信息（Script Info）增加了 `YCbCr Matrix` 以方便按照指定的色彩空间做颜色转换，mpv 使用 `sub-ass-vsfilter-color-compat=basic` 来兼容指定的 `YCbCr Matrix`，AssRender 也做了相应适配
    - 处理：ASS 的 `YCbCr Matrix` 均指定为视频的色彩空间（一般情况下，SD 为 BT.601，HD 为 BT.709）或 `None`

8. 观看 PAR 不为 1:1 的视频时的字幕渲染
    - VSFilter 系滤镜、 `More - Renderer layout options - Use Original Video Size` 的 xySubFilter、`sub-ass-vsfilter-aspect-compat=yes` 的 mpv、Aegisub 处理字幕时会先按原始视频渲染再按指定的 DAR 拉伸
    - 处理：为避免渲染效果问题，不会基于 PAR 不为 1:1 的视频制作字幕，也不建议用 PAR 不为 1:1 的视频观看本库字幕

### 为什么改用 libass

我认为字幕制作的基本是要能达成`制作 - 压制 - 播放`三个部分渲染效果的一致，长久以来的「xy-VSFilter 体系（Aegisub 的 xy-VSFilter - [xy-VSFilter](https://github.com/HomeOfVapourSynthEvolution/xy-VSFilter) - [xySubFilter](https://github.com/pinterf/xy-VSFilter)）」确实能较好地实现，虽然某种程度上牺牲了非 Windows 平台用户的体验（如某些标签、字体错误渲染的「负负得正」）。同时 Aegisub 年久失修以及编译繁杂、libass 在 2017 年的 0.14.0 之后一直没有新的 release、同样基于 libass 的 Aegisub 和 Vapoursynth 的 Subtext 会得出不同的渲染效果，我难以达成简便统一的 libass 三端体验。期间我对 mpv 的尝试认识到了它优良的播放环境。

得益于 Aegisub wangqr fork 解决了不少 r8942 以来的 bug 提高了我的字幕制作体验，对编译流程的梳理和使用动态链接库让更新 libass 滤镜变得便捷。libass 0.15.0 的发布让我对繁杂的 libass 环境有了信心，但此时的 libass 仍会因为系统字体库的庞大而占用大量的时间加载字体，Apache553 的「[按需加载字体](https://github.com/libass/libass/pull/477)」解决了这个问题。同时 Masaiki（菜姬）把 AssRender 移植到了 Vapoursynth，在他的帮助下我对「[新的 libass 体系](#可以正确渲染的推荐环境配置)」不断进行测试，终于确信了可以在维持「xy-VSFilter 体系」体验的同时简便地转移到 libass。

虽然 libass 还有一些问题，但体验与 VSFilter 系相比已经好了不少，在将来也会在一些 VSFilter 系没有错误的渲染效果上向其靠拢，同时 mpv 也可以模拟以配合 VSFilter 系的积重难返。