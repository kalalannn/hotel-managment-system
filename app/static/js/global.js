class Utils {
    static showToast(type, message) {
        if (type === 'success') {
            toastr.success(message);
        } else if (type === 'warning') {
            toastr.warning(message);
        } else if (type = 'error') {
            toastr.error(message);
        } else {
            toastr.info(message);
        }
    }
}