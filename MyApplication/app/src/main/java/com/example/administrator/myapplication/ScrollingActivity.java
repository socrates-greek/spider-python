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
import android.view.MotionEvent;
import android.view.View;
import android.webkit.WebSettings;
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
    private Long userArticleId;


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
        userArticleId = bundle.getLong("userArticleId");

        textviewcontent.getSettings().setDefaultTextEncodingName("UTF -8");//设置默认为utf-8
        textviewcontent.loadData(content, "text/html; charset=UTF-8", null);//这种写法可以正确解码

        // 是否支持脚本
        textviewcontent.getSettings().setJavaScriptEnabled(true);
        //支持缩放
        textviewcontent.getSettings().setSupportZoom(true);
        textviewcontent.getSettings().setMinimumFontSize(20);
        //自动适应屏幕
        //textviewcontent.getSettings().setLoadWithOverviewMode(true);
        //textviewcontent.getSettings().setUseWideViewPort(true);


        textviewcontent.setOnTouchListener(new View.OnTouchListener() {
            float OldX1,OldY1,OldX2,OldY2,NewX1,NewY1,NewX2,NewY2;
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                // TODO Auto-generated method stub
                switch (event.getAction()) {
                    case MotionEvent.ACTION_POINTER_2_DOWN:
                        if (event.getPointerCount() == 2) {
                            for (int i = 0; i < event.getPointerCount(); i++) {
                                if (i == 0) {
                                    OldX1 = event.getX(i);
                                    OldY1 = event.getY(i);
                                } else if (i == 1) {
                                    OldX2 = event.getX(i);
                                    OldY2 = event.getY(i);
                                }
                            }
                        }
                        break;
                    case MotionEvent.ACTION_MOVE:
                        if (event.getPointerCount() == 2) {
                            for (int i = 0; i < event.getPointerCount(); i++) {
                                if (i == 0) {
                                    NewX1 = event.getX(i);
                                    NewY1 = event.getY(i);
                                } else if (i == 1) {
                                    NewX2 = event.getX(i);
                                    NewY2 = event.getY(i);
                                }
                            }
                            float disOld = (float) Math.sqrt((Math.pow(OldX2 - OldX1, 2) + Math.pow(
                                    OldY2 - OldY1, 2)));
                            float disNew = (float) Math.sqrt((Math.pow(NewX2 - NewX1, 2) + Math.pow(
                                    NewY2 - NewY1, 2)));
                            Log.d("onTouch","disOld="+disOld+"|disNew="+disNew);
                            if (disOld - disNew >= 25) {
                                // 缩小
                                textviewcontent.zoomOut();

                            } else if(disNew - disOld >= 25){
                                // 放大
                                textviewcontent.zoomIn();
                            }
                            OldX1 = NewX1;
                            OldX2 = NewX2;
                            OldY1 = NewY1;
                            OldY2 = NewY2;
                        }
                }
                return false;
            }
        });


        //webview 长按事件
        textviewcontent.setOnCreateContextMenuListener(new View.OnCreateContextMenuListener(){

            public void onCreateContextMenu(ContextMenu menu, View arg1,
                                            ContextMenu.ContextMenuInfo arg2) {
                MenuItem.OnMenuItemClickListener handler = new MenuItem.OnMenuItemClickListener() {
                    public boolean onMenuItemClick(MenuItem item) {
                        switch(item.getItemId()){
                            case WEB_FenXiang:
                                Log.i("you click","删除");
                                String result= ServiceUtil.getServiceInfo(Constants.deleteUserArticle+userArticleId,Constants.ip,Constants.port);
                                if ("success".equals(result)){
                                    Toast.makeText(ScrollingActivity.this, "你把我丢掉了，小主人！", Toast.LENGTH_SHORT).show();
                                    finish();
                                }

                                break;
                            case WEB_XiaZai:
                                Log.i("you click","已读");
                                String result2= ServiceUtil.getServiceInfo(Constants.modifyRead+userArticleId,Constants.ip,Constants.port);
                                if ("success".equals(result2)){
                                    Toast.makeText(ScrollingActivity.this, "你又进步了，小主人！", Toast.LENGTH_SHORT).show();
                                    finish();
                                }

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

                    item = menu.add(0,WEB_XiaZai, 0,"已读").setOnMenuItemClickListener(handler); ;
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
