import pandas as pd
import math

df = pd.read_csv('chain.csv')

a = df['Tahun'].tolist()
b = df['Bulan'].tolist()
c = df['Harga(rupiah)'].tolist()

#dMax, dMin, d1, d2
dMax = max(c)
lstDMax = [' ']*len(c)
lstDMax[0] = dMax

dMin = min(c)
lstDMin = [' ']*len(c)
lstDMin[0] = dMin

d1 = 50
d2 = 50
u = [dMin-d2, dMax+d1]

# Jumlah Interval 
interval = round(1+(3.322*math.log(len(c),10)))
lstInterval = [' ']*len(c)
lstInterval[0] = interval

# Panjang Interval
intervalLength = round((u[1]-u[0])/interval)
lstIntervalLength = [' ']*len(c)
lstIntervalLength[0] = intervalLength

def intervalTable(min, intervalLength, numClass):
  lst = []
  for i in range(numClass):
    lst.append([])

  for i in range(numClass):
    if i == 0:
      lst[i].append(min)
      lst[i].append("A"+str(i+1))
      lst[i].append(min+intervalLength)
      lst[i].append(int((lst[i][0]+lst[i][2])/2))
    else:
      lst[i].append(lst[i-1][2])
      lst[i].append("A"+str(i+1))
      lst[i].append(lst[i-1][2]+intervalLength)
      lst[i].append(int((lst[i][0]+lst[i][2])/2))

  return lst

def fuzzyfy(listIntervalTable ,c):
  lst = []
  for i in c:
    for x in listIntervalTable:
      if i >= x[0] and i <= x[2]:
        lst.append(x[1])
  return lst

def flr(listFuzzyfy):
  lst = []
  for i in range(len(listFuzzyfy)):
    lst.append([])

  for i in range(len(listFuzzyfy)):
    if i == len(listFuzzyfy)-1:
      lst[i].append(listFuzzyfy[i])
      lst[i].append(listFuzzyfy[i])
    else:
      lst[i].append(listFuzzyfy[i])
      lst[i].append(listFuzzyfy[i+1])

  return lst

def convertFLR(tempFLR):
  lst = []
  for i in tempFLR:
    lst.append(i[0]+">"+i[1])
  return lst

def flrg(listIntervalTable,tempFLR):
  curr = []
  for i in listIntervalTable:
    curr.append(i[1])

  tempNext = []
  for i in range(len(listIntervalTable)):
    tempNext.append([])
  for i in range(len(tempNext)):
    for x in tempFLR:
      if curr[i] == x[0] and x[1]:
        tempNext[i].append(x[1])
    tempNext[i].sort(key= lambda x: (len(x), x))

  sumNext = []
  for i in listIntervalTable:
    sumNext.append([])

  for i in range(len(tempNext)):
    for x in listIntervalTable:
      sumNext[i].append(tempNext[i].count(x[1]))

  tempNext2 = []
  for i in range(len(listIntervalTable)):
    tempNext2.append([])
  for i in range(len(tempNext2)):
    for x in tempFLR:
      if curr[i] == x[0] and x[1] not in tempNext2[i]:
        tempNext2[i].append(x[1])
    tempNext2[i].sort(key= lambda x: (len(x), x))

  next = []
  for i in range(len(tempNext2)):
    str = ""
    str = ", ".join(tempNext2[i])
    next.append(str)
  return list(zip(curr, next)), list(zip(curr, tempNext2, sumNext)), sumNext

def matrixWght(lstMatrix):
  lst = []
  for i in lstMatrix:
    lst.append([])
  
  for i in range(len(lstMatrix)):
    for x in lstMatrix[i]:
      if x == 0:
        lst[i].append(0)
      else:
        lst[i].append(round(x/sum(lstMatrix[i]), 2))
      # print(round(x/sum(lstMatrix[i]), 2))
  return lst

def forecastResult(lstTempFLRG, listIntervalTable, lstMatrixWght):
  lst = []

  for i in range(len(lstMatrixWght)):
    res = 0
    for x in range(len(lstMatrixWght)):
      # print(listIntervalTable[x])
      res += listIntervalTable[x][3]*lstMatrixWght[i][x]
    lst.append(round(res))
  return lst

def intervalClass(listIntervalTable):
  lst = []
  for i in listIntervalTable:
    lst.append(i[1])
  return lst

def forecast(lstTempFLRG, lstFuzzyfy, lstForecastResult):
  lst = []
  lst.append(0)
  for i in range(1, len(lstFuzzyfy)):
    for x in lstTempFLRG:
      if lstFuzzyfy[i] == x[0]:
        lst.append(lstForecastResult[lstTempFLRG.index(x)])
        break

  return lst

def adjust(tempFLR, lstFLRG, n):
  lst = []
  lst.append(0)

  temp = []
  for i in lstFLRG:
    temp.append(i[0])

  for i in range(1, len(tempFLR)):
    if tempFLR[i-1][0] == tempFLR[i-1][1]:
      lst.append(0)
    elif tempFLR[i-1][0] > tempFLR[i-1][1]:
      left = temp.index(tempFLR[i-1][0])
      right = temp.index(tempFLR[i-1][1])

      lst.append(-(round(n*(left-right))))
    else:
      left = temp.index(tempFLR[i-1][0])
      right = temp.index(tempFLR[i-1][1])

      lst.append(round(n*(right-left)))
  return lst

def finalForecast(lstForecast,lstAdjust):
  lst = []
  for i in range(len(lstForecast)):
    lst.append(lstForecast[i]+lstAdjust[i])
  return lst

def forecastDiff(c, lstFinalForecast):
  lst = []
  lst.append(0)
  for i in range(1, len(c)):
    lst.append(abs(c[i]-lstFinalForecast[i]))
  return lst

def finalForecastDiff(c, lstForecastDiff):
  lst = []
  lst.append(0)
  for i in range(1, len(c)):
    lst.append(round((lstForecastDiff[i]/c[i])*100, 5))
  return lst

def NextPredict(num, lstTempFLRG, lstForecastResult):
  for i in lstTempFLRG:
    if num == i[0]:
      return lstForecastResult[lstTempFLRG.index(i)]


# Tabel Interval
listIntervalTable = intervalTable(u[0], intervalLength, interval)
dfIntervalTable = pd.DataFrame(listIntervalTable)

# Class
lstIntervalClass = intervalClass(listIntervalTable)

# Fuzzyfikasi
lstFuzzyfy = fuzzyfy(listIntervalTable ,c)
dfFuzzyfy = pd.DataFrame(lstFuzzyfy, columns = ["Fuzzyfikasi"])

# FLR
tempFLR = flr(lstFuzzyfy)
lstFLR = convertFLR(tempFLR)
dfFLR = pd.DataFrame(lstFLR, columns = ["FLR"])

# FLRG & Matrix
lstFLRG, lstTempFLRG, lstMatrix = flrg(listIntervalTable,tempFLR)
dflstFLRG = pd.DataFrame(lstFLRG)

# Bobot Matrix
lstMatrixWght = matrixWght(lstMatrix)
dflstMatrixWght = pd.DataFrame(lstMatrixWght,columns = lstIntervalClass)
dflstMatrixWght[" "] = lstIntervalClass
dflstMatrixWght.set_index(" ", inplace=True)

# Hasil Peramalan
lstForecastResult = forecastResult(lstTempFLRG, listIntervalTable, lstMatrixWght) 
dflstForecastResult = pd.DataFrame(lstForecastResult, columns = ["Hasil Peramalan"])

# Ramalan 1
lstForecast = forecast(lstTempFLRG, lstFuzzyfy, lstForecastResult)
dflstForecast = pd.DataFrame(lstForecast, columns = ["Ramalan 1"])

# Adjust
lstAdjust = adjust(tempFLR, lstFLRG, intervalLength/2)
dflstAdjust = pd.DataFrame(lstAdjust, columns = ["Adjust"])

# Ramalan Akhir
lstFinalForecast = finalForecast(lstForecast,lstAdjust)
dflstFinalForecast = pd.DataFrame(lstFinalForecast, columns = ["Ramalan Akhir"])

# |At-Ft|
lstForecastDiff = forecastDiff(c, lstFinalForecast)
dflstForecastDiff = pd.DataFrame(lstForecastDiff, columns = ["|At-Ft|"])

# |At-Ft|/At
lstFinalForecastDiff = finalForecastDiff(c, lstForecastDiff)
dflstFinalForecastDiff = pd.DataFrame(lstFinalForecastDiff, columns = ["|At-Ft|/At"])

# total |At-Ft|/At
totalFinalForecastDiff = sum(lstFinalForecastDiff)
lstTotalFinalForecastDiff = [' ']*len(c)
lstTotalFinalForecastDiff[0] = totalFinalForecastDiff

# Mape
mape = round(100-(totalFinalForecastDiff/len(lstFinalForecastDiff)), 2)
lstMape = [' ']*len(c)
lstMape[0] = mape

nextPredict = NextPredict(tempFLR[len(tempFLR)-1][1], lstTempFLRG, lstForecastResult)
lstNextPredict = [' ']*len(c)
lstNextPredict[0] = nextPredict

# to Excel
final = pd.concat([df, dfFuzzyfy, dfFLR, dflstForecast, dflstAdjust, dflstFinalForecast, dflstForecastDiff, dflstFinalForecastDiff], axis = 1)
final['Total'] = lstTotalFinalForecastDiff
final['Ramalan Selanjutnya'] = lstNextPredict
final['MAPE'] = lstMape
final['Harga Terbesar'] = lstDMax
final['Harga Terkecil'] = lstDMin
final['Panjang Interval'] = lstIntervalLength
final['Jumlah Interval'] = lstInterval
final[' '] = [' ']*len(c)
final['Minimum'] = dfIntervalTable[0]
final['Minimum'] = final['Minimum'].fillna('')

final['Kelas'] = dfIntervalTable[1]
final['Kelas'] = final['Kelas'].fillna('')

final['Maksimum'] = dfIntervalTable[2]
final['Maksimum'] = final['Maksimum'].fillna('')

final['Median'] = dfIntervalTable[3]
final['Median'] = final['Median'].fillna('')

final['  '] = [' ']*len(c)

final['Current State'] = dflstFLRG[0]
final['Current State'] = final['Current State'].fillna('')

final['Next State'] = dflstFLRG[1]
final['Next State'] = final['Next State'].fillna('')

final['Hasil Peramalan'] = dflstForecastResult
final['Hasil Peramalan'] = final['Hasil Peramalan'].fillna('')

writer = pd.ExcelWriter('result.xlsx', engine='xlsxwriter')
final.to_excel(writer, sheet_name='Main', index = False)
dflstMatrixWght.to_excel(writer, sheet_name='Matrix')

writer.save()

def showToConsole(final):
  final = final.loc[ : , final.columns != 'Fuzzyfikasi']
  final = final.loc[ : , final.columns != 'FLR']
  return final
print(showToConsole(final))
print()
print(pd.concat([pd.DataFrame(a), dfFuzzyfy, dfFLR], axis = 1))