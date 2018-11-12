package com.godzilla.cn.godzilla.service.serviceImp;

import com.godzilla.cn.godzilla.bean.Article;
import com.godzilla.cn.godzilla.bean.Disease;
import com.godzilla.cn.godzilla.bean.Drug;
import com.godzilla.cn.godzilla.mapper.ArticleMapper;
import com.godzilla.cn.godzilla.mapper.DiseaseMapper;
import com.godzilla.cn.godzilla.mapper.DrugMapper;
import com.godzilla.cn.godzilla.service.ArticleService;
import com.godzilla.cn.godzilla.service.DiseaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class DiseaseServiceImp implements DiseaseService {

    @Autowired
    private DiseaseMapper diseaseMapper;
    @Autowired
    private DrugMapper drugMapper;
    @Override
    public List<Disease> findLists(String id, Long le) {
        return diseaseMapper.findLists(id,le);
    }

    @Override
    public List<Disease> findFirstLists(Long le) {
        return diseaseMapper.findFirstLists(le);
    }

    @Override
    public List<Drug> findLists(String id) {
        return drugMapper.findLists(id);
    }

    @Override
    public List<Drug> findFirstLists() {
        return drugMapper.findFirstLists();
    }

    @Override
    public int update(String pid, long kid) {
        return diseaseMapper.update(pid,kid);
    }

    @Override
    public int updateDrug(String gg, long id) {
        return drugMapper.updateDrug(gg,id);
    }
}


