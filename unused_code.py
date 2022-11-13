from skimage.metrics import structural_similarity as compare_ssim
import d3dshot


def take_slow_screen_shot(file_name):
    os.system(f"""
        powershell.exe \"
            Add-Type -AssemblyName System.Windows.Forms
            [Windows.Forms.Sendkeys]::SendWait('+{{Prtsc}}')
            \$img = [Windows.Forms.Clipboard]::GetImage()
            \$img.Save(\\\"\$env:USERPROFILE\\AppData\\Local\\Packages\\CanonicalGroupLimited.Ubuntu20.04LTS_79rhkp1fndgsc\\LocalState\\rootfs\\home\\oliverbrace\\epistory_code\\epi_screenshots\\{file_name}\\\", [Drawing.Imaging.ImageFormat]::Jpeg)\"
    """)


def find_imgs_diff(img1, img2, openCV=True):
    (score, diff) = compare_ssim(img1, img2, full=True)
    return (diff * 255).astype("uint8")


def d3dshot_screenshot(width=None, height=None):
    if not width:
        width, _ = pyautogui.size()

    if not height:
        _, height = pyautogui.size()

    d = d3dshot.create(capture_output="numpy")
    d.display.resolution = (width, height)
    d.capture()
    img1 = d.screenshot()
    img2 = d.screenshot()
    d.stop()

    return img1, img2


def pil_image_to_opencv(image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def take_and_compare_screenshot(delay=0):
    wincap = WindowCapture('Epistory')

    img1 = wincap.get_screenshot()
    if delay:
        sleep(delay)
    img2 = wincap.get_screenshot()

    gray1 = create_gray(img1)
    gray2 = create_gray(img2)

    diff_img = find_imgs_diff(gray1, gray2)

    # save_image("img1", img1)
    # save_image("img2", img2)
    # save_image("diff_img", diff_img)

    return img2, diff_img
