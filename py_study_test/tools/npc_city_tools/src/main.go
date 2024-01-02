package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"os"
	"strconv"
)

// 主函数
func main() {
	// 读json
	file, err := ioutil.ReadFile("./CustomRiverCity.json")
	if err != nil {
		//log.Fatalf("请将文件CustomRiverCity.json 和工具放到一个文件夹中")
		log.Fatalf("读取json文件失败", err)
		return
	}
	cConf := CityConf{}
	// 解析json文件
	err = json.Unmarshal(file, &cConf)
	if err != nil {
		log.Fatalf("解析json文件失败", err)
		return
	}

	// 删除输出文件
	_ = os.Remove("./out.txt")

	f, err := os.OpenFile("./out.txt", os.O_CREATE|os.O_APPEND|os.O_RDWR|os.O_SYNC, 0660)

	// 最后关闭文件
	defer f.Close()

	// 按照规则输出
	for _, v := range cConf.CityList {
		println(strconv.Itoa(v.Id) + "\t" + strconv.Itoa(v.Lv) + "\t" + strconv.Itoa(v.Size) + "\t" + v.Key + "\t" + v.Name + "\t" + v.PicName + "\t" + v.RoundKeys)
		line := strconv.Itoa(v.Id) + "\t" + strconv.Itoa(v.Lv) + "\t" + strconv.Itoa(v.Size) + "\t" + v.Key + "\t" + v.Name + "\t" + v.PicName + "\t" + v.RoundKeys
		_, err := f.WriteString(line+"\n")
		if nil != err {
			log.Fatalf("写入文件失败!", err)
			return
		}
	}
	// 按照规则输出
	for _, v := range cConf.RiverCityList {
		println("r" + strconv.Itoa(v.Id) + "\t" + strconv.Itoa(v.Lv) + "\t" + strconv.Itoa(v.Size) + "\t" + v.Key + "\t" + v.Name + "\t" + v.PicName + "\t" + v.RoundKeys)
		line := strconv.Itoa(v.Id) + "\t" + strconv.Itoa(v.Lv) + "\t" + strconv.Itoa(v.Size) + "\t" + v.Key + "\t" + v.Name + "\t" + v.PicName + "\t" + v.RoundKeys
		_, err := f.WriteString(line+"\n")
		if nil != err {
			log.Fatalf("写入文件失败!", err)
			return
		}
	}
}

// json文件
type CityConf struct {
	CityList      []City
	RiverCityList []RiverCity
}

// 渡口
type RiverCity struct {
	Id        int    `json:"id"`
	Lv        int    `json:"lv"`
	Size      int    `json:"size"`
	Key       string `json:"centerKey"`
	Name      string `json:"name"`
	PicName   string `json:"pic1"`
	RoundKeys string `json:"tileList"`
	Type      int `json:"type"`
}

// 城
type City struct {
	Id        int    `json:"id"`
	Lv        int    `json:"lv"`
	Size      int    `json:"size"`
	Key       string `json:"key"`
	Name      string `json:"name"`
	PicName   string `json:"picName"`
	RoundKeys string `json:"roundKeys"`
	Type      int `json:"type"`
}
