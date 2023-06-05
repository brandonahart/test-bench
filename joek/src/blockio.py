# demonstrate buffered reading & writing in python via io.BufferedReader

# generate random binary file with 10 * 4096 bytes:  dd if=/dev/urandom of=rand.bin bs=1 count=40960

# import io

fname = './data/rand.bin'


# read a buffer, print the buffer
# buffering parm on open causes return of io.BufferedReader

inf = open(fname,'rb',buffering=10)
print("type = {}".format(type(inf)))
b = inf.read(10)
print("len = {}".format(len(b)))
print("bytes = {}".format(b))
inf.close()

print("===")


# read the file a buffer at a time while monitoring each read 

cnt = 0 
with open(fname, 'rb', buffering=4096) as f:
    while True:
        cnt += 1
        buf = f.read(4096)
        print("buf{}: len={} buf[0:9]={}".format(cnt,len(buf),buf[0:9]))
        if len(buf) == 0:
            break


# read the file a buffer at a time and write a new copy of the file a buffer at a time.
# to verify results are equal use: diff data/rand.bin data/rand_copy.bin 

bsize = 4096
with open(fname, 'rb', buffering=bsize) as inf:
    with open('./data/rand_copy.bin','wb',buffering=bsize) as outf:
        while True:
            buf = inf.read(bsize)
            if len(buf) > 0:
                outf.write(buf)
            else:
                break
                





