#coding=utf-8
'''
batchLpf.py ��Ӧ���ýű�
������ô�Ĳ���
'''

#acc, gyro, mag, rotation
#���赥���� mag �˲��� �� sensors='m' ���ɣ� Ĭ���ĸ�ȫ�˲�
sensors='agmr'

assert set(sensors) <= set('agmr'), "must be combinations of char 'a', 'g', 'm', 'r'"


#LPF hamming ���ڳ���
#�� scipy.signal.firwin ���� numtaps, ��������̶�Ϊ cutoff=40, nyq=800�� �� utils.py
winsz=10


#ԭʼ����Ŀ¼��
olddir=r'D:\Documents\Desktop\t'

#�����Ŀ¼��
newdir=r'D:\Documents\Desktop\t/shit'




