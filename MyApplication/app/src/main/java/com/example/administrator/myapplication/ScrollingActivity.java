package com.example.administrator.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.app.Activity;
import android.text.Html;
import android.text.Spannable;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.style.AbsoluteSizeSpan;
import android.util.Log;
import android.view.ContextMenu;
import android.view.MenuItem;
import android.view.View;
import android.webkit.WebView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.administrator.myapplication.commom.Constants;

public class ScrollingActivity extends Activity {

    private WebView textviewcontent;
    private final int WEB_FenXiang = 0;
    private final int WEB_XiaZai = 1;
    private final int WEB_FuZhi = 2;
    private final int WEB_AddSQ = 3;
    private Long id;


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
        String title = bundle.getString("title");
        id = bundle.getLong("id");


        textviewcontent.getSettings().setDefaultTextEncodingName("UTF -8");//设置默认为utf-8
        textviewcontent.loadData(content, "text/html; charset=UTF-8", null);//这种写法可以正确解码


        //webview 长按事件
        textviewcontent.setOnCreateContextMenuListener(new View.OnCreateContextMenuListener(){

            public void onCreateContextMenu(ContextMenu menu, View arg1,
                                            ContextMenu.ContextMenuInfo arg2) {
                MenuItem.OnMenuItemClickListener handler = new MenuItem.OnMenuItemClickListener() {
                    public boolean onMenuItemClick(MenuItem item) {
                        switch(item.getItemId()){
                            case WEB_FenXiang:
                                Log.i("you click","删除");
                                String result= ServiceUtil.getServiceInfo(Constants.deleteArticle+id,Constants.ip,Constants.port);
                                if ("success".equals(result)){
                                    Toast.makeText(ScrollingActivity.this, "删除成功！", Toast.LENGTH_SHORT).show();
                                    finish();

                                }

                                break;
                            case WEB_XiaZai:
                                Log.i("you click","下载");
                                break;
                            case WEB_FuZhi:
                                Log.i("you click","复制");
                                break;
                            case WEB_AddSQ:
                                Log.i("you click","增加到书签");
                                break;
                        }
                        return true;
                    }
                };
                Log.i("long click","true");
                WebView.HitTestResult result = ((WebView) arg1).getHitTestResult();
                int resultType = result.getType();
                if ((resultType == WebView.HitTestResult.ANCHOR_TYPE) || (resultType == WebView.HitTestResult.UNKNOWN_TYPE) || (resultType == WebView.HitTestResult.SRC_ANCHOR_TYPE) ||
                        (resultType == WebView.HitTestResult.SRC_IMAGE_ANCHOR_TYPE)) {
                    Intent i = new Intent();
                    MenuItem item = menu.add(0, WEB_FenXiang, 0, "删除").setOnMenuItemClickListener(handler);
                    item.setIntent(i);
                    item = menu.add(0, WEB_FuZhi, 0, "复制").setOnMenuItemClickListener(handler);
                    item.setIntent(i);

                    item = menu.add(0,WEB_XiaZai, 0,"下载").setOnMenuItemClickListener(handler); ;
                    item.setIntent(i);

                    item = menu.add(0,WEB_AddSQ, 0,"增加到书签").setOnMenuItemClickListener(handler); ;
                    item.setIntent(i);
                    menu.setHeaderTitle(result.getExtra());
                }
                else if (resultType == WebView.HitTestResult.IMAGE_TYPE) {
                    Intent i = new Intent();
                    MenuItem item = menu.add(0, 1, 0, "OPEN");
                    item.setIntent(i);
                    item = menu.add(0, 2, 0, "图片");
                    item.setIntent(i);
                    menu.setHeaderTitle(result.getExtra());
                }
            }
        });

    }
}
