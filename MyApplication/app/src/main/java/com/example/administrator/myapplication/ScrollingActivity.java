package com.example.administrator.myapplication;

import android.os.Bundle;
import android.app.Activity;
import android.text.Html;
import android.text.Spannable;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.style.AbsoluteSizeSpan;
import android.webkit.WebView;
import android.widget.TextView;

public class ScrollingActivity extends Activity {

    private WebView textviewcontent;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scrolling);

        //textview 控件
        textviewcontent = (WebView) findViewById(R.id.detailTextView);
        //新页面接收数据
        Bundle bundle = this.getIntent().getExtras();
        //接收content值
        String content = bundle.getString("content");
        textviewcontent.getSettings().setDefaultTextEncodingName("UTF -8");//设置默认为utf-8
        textviewcontent.loadData(content, "text/html; charset=UTF-8", null);//这种写法可以正确解码
//调用

//        SpannableString spanString = new SpannableString(Html.fromHtml(content));
//        AbsoluteSizeSpan span = new AbsoluteSizeSpan(50);
//        spanString.setSpan(span, 0, 5, Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);
//        String str = spanString.toString();
//        str = str.replace("document.getElementById(\"readerFt\").className = \"rft_\" + rSetDef()[2];","");
//        str = str.replace("document.getElementById(\"readerFs\").className = \"rfs_\" + rSetDef()[3]","");
//        textviewcontent.setText(str.trim());
    }
}
