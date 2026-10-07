// win32_window.cpp — 最小骨架：DPI v2 感知窗口 + 消息循环
// 编译（Developer Command Prompt）：
//   cl /EHsc /W4 /DUNICODE /D_UNICODE win32_window.cpp user32.lib gdi32.lib shcore.lib
#include <windows.h>

static void Scale(LPRECT r, UINT dpi) {
  const float k = static_cast<float>(dpi) / 96.0f;
  r->left = static_cast<LONG>(r->left * k);
  r->top = static_cast<LONG>(r->top * k);
  r->right = static_cast<LONG>(r->right * k);
  r->bottom = static_cast<LONG>(r->bottom * k);
}

static LRESULT CALLBACK WndProc(HWND h, UINT m, WPARAM w, LPARAM l) {
  switch (m) {
    case WM_DPICHANGED: {
      // 采用系统建议矩形，并按新 DPI 重排内容（勿用像素常量）。
      RECT* const sug = reinterpret_cast<RECT*>(l);
      SetWindowPos(h, nullptr, sug->left, sug->top,
                   sug->right - sug->left, sug->bottom - sug->top,
                   SWP_NOZORDER | SWP_NOACTIVATE);
      return 0;
    }
    case WM_GETMINMAXINFO: {
      MINMAXINFO* const mmi = reinterpret_cast<MINMAXINFO*>(l);
      const UINT dpi = GetDpiForWindow(h);
      RECT work{0, 0, 1280, 720};
      SystemParametersInfoForDpi(SPI_GETWORKAREA, 0, &work, 0, dpi);
      mmi->ptMaxTrackSize.x = work.right - work.left;
      mmi->ptMaxTrackSize.y = work.bottom - work.top;
      return 0;
    }
    case WM_DESTROY:
      PostQuitMessage(0);
      return 0;
  }
  return DefWindowProc(h, m, w, l);
}

int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int show) {
  // DPI 感知必须在创建任何窗口之前确定（亦可写进 app.manifest）。
  SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2);
  WNDCLASS wc{};
  wc.lpfnWndProc = WndProc;
  wc.hInstance = inst;
  wc.lpszClassName = L"WinAppDevExpertWindow";
  if (!RegisterClass(&wc)) {
    return static_cast<int>(GetLastError());
  }
  HWND hwnd = CreateWindowEx(0, wc.lpszClassName, L"windows-app-dev-expert sample",
                             WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
                             640, 480, nullptr, nullptr, inst, nullptr);
  if (!hwnd) {
    return static_cast<int>(GetLastError());
  }
  ShowWindow(hwnd, show);
  MSG msg{};
  while (GetMessage(&msg, nullptr, 0, 0) > 0) {  // <=0 含错误与 WM_QUIT，须区分
    TranslateMessage(&msg);
    DispatchMessage(&msg);
  }
  (void)Scale;  // 示例保留：实际内容布局按 dpi/96 换算
  return static_cast<int>(msg.wParam);
}
