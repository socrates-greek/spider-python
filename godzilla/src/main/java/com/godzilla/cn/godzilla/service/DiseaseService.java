package com.godzilla.cn.godzilla.service;

import com.godzilla.cn.godzilla.bean.Article;
import com.godzilla.cn.godzilla.bean.Disease;
import com.godzilla.cn.godzilla.bean.Drug;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface DiseaseService {
    List<Disease> findLists(String id,Long le);
    List<Disease> findFirstLists(Long  le);

    List<Drug> findLists(String id);
    List<Drug> findFirstLists();
    int update(String pid,long id);
    int updateDrug(String gg,long id);


}
