package com.example.administrator.myapplication;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.Map;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import android.annotation.SuppressLint;
import android.os.StrictMode;
import android.util.Log;

@SuppressLint("NewApi")
public class ServiceUtil {
    public static String userAgent =  "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36";
    public static String getServiceInfo  (String strUrl,String ip,String port)
    {
        System.setProperty("https.proxyHost", ip);
        System.setProperty("https.proxyPort", port);
        StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder().detectDiskReads().detectDiskWrites().detectNetwork().penaltyLog().build());
        StrictMode.setVmPolicy(new StrictMode.VmPolicy.Builder().detectLeakedSqlLiteObjects().detectLeakedClosableObjects().penaltyLog().penaltyDeath().build());
        HttpURLConnection conn = null;
        BufferedReader reader = null;
        InputStream ips = null;
        String rs = null;
        try {
            StringBuffer sb = new StringBuffer();
            URL url = new URL(strUrl);
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("User-agent", userAgent);
            conn.setUseCaches(false);
            conn.setConnectTimeout(90000);
            conn.setReadTimeout(90000);
            conn.setInstanceFollowRedirects(false);
            conn.connect();
            ips = conn.getInputStream();
            reader = new BufferedReader(new InputStreamReader(ips, "UTF-8"));
            String strRead = null;
            while ((strRead = reader.readLine()) != null) {
                sb.append(strRead);
            }
            rs = sb.toString();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            if(ips!=null){
                try {
                    ips.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            if (conn != null) {
                conn.disconnect();
            }
        }
        if(null!=rs){
            rs = rs;
        }
        return rs;
    }

    /**
     * post请求获取数据
     * @param strUrl 请求地址，如： "http://....asmx/HelloWork"
     * @param params 设置发送的参数，如："key=1&name=1";//设置发送的参数
     * @return
     */
    public  String getServiceInfoPost(String strUrl,String params)
    {
        String strResult="";
        ExecutorService threadPool= Executors.newSingleThreadExecutor();
        Future<String> future=threadPool.submit(new CallableImpl(strUrl,params));
        System.out.println("----------");
        try {
            System.out.println(future.get());
            strResult = future.get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }

        return strResult;
    }


    class CallableImpl implements Callable {
        public String strUrl;
        public String params;
        public CallableImpl(String url,String params){
            this.params=params;
            this.strUrl = url;
        }
        @Override
        public Object call() throws Exception {
            String strResult=null;
            try{
                byte[] data = params.toString().getBytes();
                HttpURLConnection httpURLConnection = (HttpURLConnection) new URL(strUrl).openConnection();
                httpURLConnection.setConnectTimeout(5000);       //设置连接超时时间
                httpURLConnection.setDoInput(true);                  //打开输入流，以便从服务器获取数据
                httpURLConnection.setDoOutput(true);                 //打开输出流，以便向服务器提交数据
                httpURLConnection.setRequestMethod("POST");     //设置以Post方式提交数据
                httpURLConnection.setUseCaches(false);               //使用Post方式不能使用缓存
                //设置请求体的类型是文本类型
                httpURLConnection.setRequestProperty("Content-Type", "application/json");
                //设置请求体的长度
                httpURLConnection.setRequestProperty("Content-Length", String.valueOf(data.length));
                //获得输出流，向服务器写入数据
                OutputStream outputStream = httpURLConnection.getOutputStream();
                outputStream.write(data);
                int code =httpURLConnection.getResponseCode();//响应代码 200表示成功
                if(code==200){
                    InputStream inStream = httpURLConnection.getInputStream();
                    strResult=new String(readInputStream(inStream), "UTF-8");
                    if(null!=strResult){
                        strResult = strResult.replace( "<boolean xmlns=\"http://tempuri.org/\">", "")
                                .replace("</boolean>", "")
                                .replace("</string>", "").replace("\r", "")
                                .replace("\n", "")
                                .replace("<string xmlns=\"http://tempuri.org/\" />", "");
                    }
                }
            } catch(Exception ex){
                ex.printStackTrace();
            }

            return strResult;
        }
    }


    /**
     * 从输入流中读取数据
     * @param inStream
     * @return
     * @throws Exception
     */
    public static byte[] readInputStream(InputStream inStream) {
        try{
            ByteArrayOutputStream outStream = new ByteArrayOutputStream();
            byte[] buffer = new byte[10000];
            int len = 0;
            while( (len = inStream.read(buffer)) !=-1 ){
                outStream.write(buffer, 0, len);
            }
            byte[] data = outStream.toByteArray();//网页的二进制数据
            outStream.close();
            inStream.close();
            return data;
        }
        catch(Exception ex){
            return null;
        }
    }

}