package __PACKAGE__;

import android.content.ActivityNotFoundException;
import android.content.ClipData;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import androidx.core.content.FileProvider;
import android.graphics.pdf.PdfRenderer;
import android.os.Bundle;
import android.os.CancellationSignal;
import android.os.ParcelFileDescriptor;
import android.print.PageRange;
import android.print.PrintAttributes;
import android.print.PrintDocumentAdapter;
import android.print.PrintDocumentInfo;
import android.print.PrintManager;
import android.util.Base64;

import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;

/**
 * Sends a PDF (base64) straight to Android's system print dialog, so bills can be printed on any printer the phone
 * can reach (Wi-Fi, USB, Bluetooth, "Save as PDF"). Added to the generated Android project by native/patch-android.py.
 */
@CapacitorPlugin(name = "ZXPrint")
public class ZXPrintPlugin extends Plugin {

    private static final int MAX_BYTES = 40 * 1024 * 1024;

    /** Opens the customer's WhatsApp chat with the PDF/image already attached (jid = phone number). Rejects if WhatsApp is missing so the app falls back to the share sheet. */
    @PluginMethod
    public void sendWhatsApp(final PluginCall call) {
        final String b64 = call.getString("data");
        final String mime = call.getString("mime", "application/octet-stream");
        final String text = call.getString("text", "");
        final String digits = call.getString("phone", "").replaceAll("\\D", "");
        final String name = call.getString("name", "Ad ZoneX").replaceAll("[^\\w .\\-]", "-");
        if (b64 == null || b64.isEmpty()) {
            call.reject("No file to send.");
            return;
        }
        final Uri uri;
        try {
            byte[] bytes = Base64.decode(b64, Base64.DEFAULT);
            if (bytes.length < 8 || bytes.length > MAX_BYTES) {
                call.reject("The file is empty or too large.");
                return;
            }
            File dir = new File(getContext().getCacheDir(), "wa");
            dir.mkdirs();
            File[] old = dir.listFiles();
            if (old != null) for (File f : old) f.delete();
            File file = new File(dir, name);
            try (OutputStream out = new FileOutputStream(file)) {
                out.write(bytes);
            }
            uri = FileProvider.getUriForFile(getContext(), getContext().getPackageName() + ".fileprovider", file);
        } catch (Exception e) {
            call.reject("Could not prepare the file: " + e.getMessage());
            return;
        }
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                String[] pkgs = {"com.whatsapp", "com.whatsapp.w4b"};
                for (String pkg : pkgs) {
                    try {
                        Intent i = new Intent(Intent.ACTION_SEND);
                        i.setType(mime);
                        i.putExtra(Intent.EXTRA_STREAM, uri);
                        if (!text.isEmpty()) i.putExtra(Intent.EXTRA_TEXT, text);
                        if (!digits.isEmpty()) i.putExtra("jid", digits + "@s.whatsapp.net");
                        i.setClipData(ClipData.newRawUri("", uri));
                        i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                        i.setPackage(pkg);
                        getActivity().startActivity(i);
                        call.resolve();
                        return;
                    } catch (ActivityNotFoundException e) {
                        // try the next WhatsApp variant
                    } catch (Exception e) {
                        call.reject("Could not open WhatsApp: " + e.getMessage());
                        return;
                    }
                }
                call.reject("WhatsApp is not installed.");
            }
        });
    }

    @PluginMethod
    public void printPdf(final PluginCall call) {
        final String b64 = call.getString("data");
        final String rawName = call.getString("name", "Ad ZoneX");
        if (b64 == null || b64.isEmpty()) {
            call.reject("No PDF data to print.");
            return;
        }
        final String name = rawName.replaceAll("[^\\w .\\-]", "-");
        final File file;
        try {
            byte[] bytes = Base64.decode(b64, Base64.DEFAULT);
            if (bytes.length < 8 || bytes.length > MAX_BYTES || bytes[0] != '%' || bytes[1] != 'P' || bytes[2] != 'D' || bytes[3] != 'F') {
                call.reject("This is not a valid PDF.");
                return;
            }
            file = new File(getContext().getCacheDir(), "print-" + System.currentTimeMillis() + ".pdf");
            try (OutputStream out = new FileOutputStream(file)) {
                out.write(bytes);
            }
        } catch (Exception e) {
            call.reject("Could not prepare the PDF: " + e.getMessage());
            return;
        }
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                try {
                    PrintManager pm = (PrintManager) getActivity().getSystemService(Context.PRINT_SERVICE);
                    PrintAttributes attrs = new PrintAttributes.Builder()
                            .setMediaSize(PrintAttributes.MediaSize.ISO_A4)
                            .setMinMargins(PrintAttributes.Margins.NO_MARGINS)
                            .build();
                    pm.print(name, new PdfAdapter(file, name), attrs);
                    call.resolve();
                } catch (Exception e) {
                    file.delete();
                    call.reject("Could not open the print dialog: " + e.getMessage());
                }
            }
        });
    }

    /** Streams an existing PDF file to the print framework. */
    static class PdfAdapter extends PrintDocumentAdapter {
        private final File file;
        private final String name;

        PdfAdapter(File file, String name) {
            this.file = file;
            this.name = name;
        }

        private int pageCount() {
            try (ParcelFileDescriptor fd = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY);
                 PdfRenderer r = new PdfRenderer(fd)) {
                return r.getPageCount();
            } catch (Exception e) {
                return PrintDocumentInfo.PAGE_COUNT_UNKNOWN;
            }
        }

        @Override
        public void onLayout(PrintAttributes oldAttributes, PrintAttributes newAttributes, CancellationSignal cancellationSignal,
                             LayoutResultCallback callback, Bundle extras) {
            if (cancellationSignal.isCanceled()) {
                callback.onLayoutCancelled();
                return;
            }
            PrintDocumentInfo info = new PrintDocumentInfo.Builder(name + ".pdf")
                    .setContentType(PrintDocumentInfo.CONTENT_TYPE_DOCUMENT)
                    .setPageCount(pageCount())
                    .build();
            callback.onLayoutFinished(info, true);
        }

        @Override
        public void onWrite(PageRange[] pages, ParcelFileDescriptor destination, CancellationSignal cancellationSignal,
                            WriteResultCallback callback) {
            try (InputStream in = new FileInputStream(file); OutputStream out = new FileOutputStream(destination.getFileDescriptor())) {
                byte[] buf = new byte[16384];
                int n;
                while ((n = in.read(buf)) > 0) {
                    if (cancellationSignal.isCanceled()) {
                        callback.onWriteCancelled();
                        return;
                    }
                    out.write(buf, 0, n);
                }
                callback.onWriteFinished(new PageRange[]{PageRange.ALL_PAGES});
            } catch (Exception e) {
                callback.onWriteFailed(e.toString());
            }
        }

        @Override
        public void onFinish() {
            file.delete();
        }
    }
}
